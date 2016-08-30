import os
import signal
import subprocess
import threading
import time
import sys
import string


_abort_on_error = False

def SetAbortOnError(abort=True):
  """Sets behavior of RunCommand to throw AbortError if command process returns
  a negative error code"""
  global _abort_on_error
  _abort_on_error = abort

def RunCommand(cmd, timeout_time=None, retry_count=3, return_output=True,
               stdin_input=None):
  """Spawn and retry a subprocess to run the given shell command.

  Args:
    cmd: shell command to run
    timeout_time: time in seconds to wait for command to run before aborting.
    retry_count: number of times to retry command
    return_output: if True return output of command as string. Otherwise,
      direct output of command to stdout.
    stdin_input: data to feed to stdin
  Returns:
    output of command
  """
  result = None
  while True:
    try:
      result = RunOnce(cmd, timeout_time=timeout_time,
                       return_output=return_output, stdin_input=stdin_input)
    except WaitForResponseTimedOutError:
      if retry_count == 0:
        raise
      retry_count -= 1
      Log("No response for %s, retrying" % cmd)
    else:
      # Success
      #print result
      return result
  

def RunOnce(cmd, timeout_time=None, return_output=True, stdin_input=None):
  """Spawns a subprocess to run the given shell command.

  Args:
    cmd: shell command to run
    timeout_time: time in seconds to wait for command to run before aborting.
    return_output: if True return output of command as string. Otherwise,
      direct output of command to stdout.
    stdin_input: data to feed to stdin
  Returns:
    output of command
  Raises:
    errors.WaitForResponseTimedOutError if command did not complete within
      timeout_time seconds.
    errors.AbortError is command returned error code and SetAbortOnError is on.
  """
  start_time = time.time()
  so = []
  pid = []
  global _abort_on_error, error_occurred
  error_occurred = False

  def Run():
    global error_occurred
    if return_output:
      output_dest = subprocess.PIPE
    else:
      # None means direct to stdout
      output_dest = None
    if stdin_input:
      stdin_dest = subprocess.PIPE
    else:
      stdin_dest = None
    if sys.platform == 'win32':
      pipe = subprocess.Popen(
          cmd,
          stdin=stdin_dest,
          stdout=output_dest,
          stderr=subprocess.STDOUT,
          shell=True)
      
    else:
      pipe = subprocess.Popen(
          cmd,
          executable='/bin/bash',
          stdin=stdin_dest,
          stdout=output_dest,
          stderr=subprocess.STDOUT,
          shell=True)
    pid.append(pipe.pid)
    try:
      output = pipe.communicate(input=stdin_input)[0]
      if output is not None and len(output) > 0:
        so.append(output)
    except OSError, e:
      SilentLog("failed to retrieve stdout from: %s" % cmd)
      Log(e)
      so.append("ERROR")
      error_occurred = True
    if pipe.returncode:
      SilentLog("Error: %s returned %d error code" %(cmd,
          pipe.returncode))
      error_occurred = True

  t = threading.Thread(target=Run)
  t.start()

  break_loop = False
  while not break_loop:
    if not t.isAlive():
      break_loop = True

    # Check the timeout
    if (not break_loop and timeout_time is not None
        and time.time() > start_time + timeout_time):
      try:
        if sys.platform == 'win32':
          import ctypes
          PROCESS_TERMINATE = 1
          handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid[0])
          ctypes.windll.kernel32.TerminateProcess(handle, -1)
          ctypes.windll.kernel32.CloseHandle(handle)
        else:
          os.kill(pid[0], signal.SIGKILL)
        
      except OSError:
        # process already dead. No action required.
        pass

      SilentLog("about to raise a timeout for: %s" % cmd)
      raise WaitForResponseTimedOutError
    if not break_loop:
      time.sleep(0.1)

  t.join()
  output = "".join(so)
  if _abort_on_error and error_occurred:
    raise AbortError(msg=output)

  return "".join(so)


"""Provides an interface to communicate with the device via the adb command.

Assumes adb binary is currently on system path.
"""


class AdbInterface:
  """Helper class for communicating with Android device via adb."""
  def __init__(self, deviceId):
      """Direct all future commands to Android target with the given serial."""
      self._target_arg = "-s %s" % deviceId


  def SendCommand(self, command_string, timeout_time=60, retry_count=3):
    """Send a command via adb.

    Args:
      command_string: adb command to run
      timeout_time: number of seconds to wait for command to respond before
        retrying
      retry_count: number of times to retry command before raising
        WaitForResponseTimedOutError
    Returns:
      string output of command

    Raises:
      WaitForResponseTimedOutError if device does not respond to command within time
    """
    
    adb_cmd = "adb %s %s" % (self._target_arg, command_string)
    SilentLog("about to run %s" % adb_cmd)
    return RunCommand(adb_cmd, timeout_time=timeout_time,
                                  retry_count=retry_count)

  def SendShellCommand(self, cmd, timeout_time=20, retry_count=3):
    """Send a adb shell command.

    Args:
      cmd: adb shell command to run
      timeout_time: number of seconds to wait for command to respond before
        retrying
      retry_count: number of times to retry command before raising
        WaitForResponseTimedOutError

    Returns:
      string output of command

    Raises:
      WaitForResponseTimedOutError: if device does not respond to command
    """
    return self.SendCommand("shell %s" % cmd, timeout_time=timeout_time,
                            retry_count=retry_count)

  def BugReport(self, path):
    """Dumps adb bugreport to the file specified by the path.

    Args:
      path: Path of the file where adb bugreport is dumped to.
    """
    bug_output = self.SendShellCommand("bugreport", timeout_time=60)
    bugreport_file = open(path, "w")
    bugreport_file.write(bug_output)
    bugreport_file.close()

  def Push(self, src, dest):
    """Pushes the file src onto the device at dest.

    Args:
      src: file path of host file to push
      dest: destination absolute file path on device
    """
    self.SendCommand("push %s %s" % (src, dest), timeout_time=60)

  def Pull(self, src, dest):
    """Pulls the file src on the device onto dest on the host.

    Args:
      src: absolute file path of file on device to pull
      dest: destination file path on host

    Returns:
      True if success and False otherwise.
    """
    # Create the base dir if it doesn't exist already
    if not os.path.exists(os.path.dirname(dest)):
      os.makedirs(os.path.dirname(dest))

    if self.DoesFileExist(src):
      self.SendCommand("pull %s %s" % (src, dest), timeout_time=60)
      return True
    else:
      Log("ADB Pull Failed: Source file %s does not exist." % src)
      return False

  def Install(self, apk_path, extra_flags):
    """Installs apk on device.

    Args:
      apk_path: file path to apk file on host
      extra_flags: Additional flags to use with adb install

    Returns:
      output of install command
    """
    return self.SendCommand("install -r %s %s" % (extra_flags, apk_path))

  def DoesFileExist(self, src):
    """Checks if the given path exists on device target.

    Args:
      src: file path to be checked.

    Returns:
      True if file exists
    """

    output = self.SendShellCommand("ls %s" % src)
    error = "No such file or directory"

    if error in output:
      return False
    return True




  def WaitForDevicePm(self, wait_time=120):
    """Waits for targeted device's package manager to be up.

    Args:
      wait_time: time in seconds to wait

    Raises:
      WaitForResponseTimedOutError if wait_time elapses and pm still does not
      respond.
    """
    Log("Waiting for device package manager...")
    self.SendCommand("wait-for-device")
    # Now the device is there, but may not be running.
    # Query the package manager with a basic command
    try:
      self._WaitForShellCommandContents("pm path android", "package:",
                                        wait_time)
    except WaitForResponseTimedOutError:
      raise WaitForResponseTimedOutError(
          "Package manager did not respond after %s seconds" % wait_time)


  def WaitForProcess(self, name, wait_time=120):
    """Wait until a process is running on the device.

    Args:
      name: the process name as it appears in `ps`
      wait_time: time in seconds to wait

    Raises:
      WaitForResponseTimedOutError if wait_time elapses and the process is
          still not running
    """
    Log("Waiting for process %s" % name)
    self.SendCommand("wait-for-device")
    self._WaitForShellCommandContents("ps", name, wait_time)

  def WaitForProcessEnd(self, name, wait_time=120):
    """Wait until a process is no longer running on the device.

    Args:
      name: the process name as it appears in `ps`
      wait_time: time in seconds to wait

    Raises:
      WaitForResponseTimedOutError if wait_time elapses and the process is
          still running
    """
    Log("Waiting for process %s to end" % name)
    self._WaitForShellCommandContents("ps", name, wait_time, invert=True)

  def _WaitForShellCommandContents(self, command, expected, wait_time,
                                   raise_abort=True, invert=False):
    """Wait until the response to a command contains a given output.

    Assumes that a only successful execution of "adb shell <command>" contains
    the substring expected. Assumes that a device is present.

    Args:
      command: adb shell command to execute
      expected: the string that should appear to consider the
          command successful.
      wait_time: time in seconds to wait
      raise_abort: if False, retry when executing the command raises an
          AbortError, rather than failing.
      invert: if True, wait until the command output no longer contains the
          expected contents.

    Raises:
      WaitForResponseTimedOutError: If wait_time elapses and the command has not
          returned an output containing expected yet.
    """
    # Query the device with the command
    success = False
    attempts = 0
    wait_period = 5
    while not success and (attempts*wait_period) < wait_time:
      # assume the command will always contain expected in the success case
      try:
        output = self.SendShellCommand(command, retry_count=1)
        if ((not invert and expected in output)
            or (invert and expected not in output)):
          success = True
      except AbortError, e:
        if raise_abort:
          raise
        # ignore otherwise

      if not success:
        time.sleep(wait_period)
        attempts += 1

    if not success:
      raise WaitForResponseTimedOutError()


  def WaitForBootComplete(self, wait_time=20, retry_count=3):
    """Waits for targeted device's bootcomplete flag to be set.

    Args:
      wait_time: time in seconds to wait
      retry_count: number of times the command needs to be re-tried
    Raises:
      WaitForResponseTimedOutError if wait_time elapses and pm still does not
      respond.
    """
    try:
        #Log("Checking device online status...")
        boot_complete = False
        self.SendCommand("wait-for-device",retry_count)
        # Now the device is there, but may not be running.
        # Query the package manager with a basic command
        
        attempts = 0
        wait_period = 5
        while not boot_complete and (attempts*wait_period) < wait_time:
          output = self.SendShellCommand("getprop dev.bootcomplete", retry_count)
          output = output.strip()
          if output == "1":
            boot_complete = True
          else:
            time.sleep(wait_period)
            attempts += 1
            
        if not boot_complete:
          raise WaitForResponseTimedOutError(
              "dev.bootcomplete flag was not set after %s seconds" % wait_time)
        return boot_complete
    except Exception,e:
        print e
        return boot_complete
        
        

  def Sync(self, retry_count=3, runtime_restart=False):
    """Perform a adb sync.

    Blocks until device package manager is responding.

    Args:
      retry_count: number of times to retry sync before failing
      runtime_restart: stop runtime during sync and restart afterwards, useful
        for syncing system libraries (core, framework etc)

    Raises:
      WaitForResponseTimedOutError if package manager does not respond
      AbortError if unrecoverable error occurred
    """
    output = ""
    error = None
    if runtime_restart:
      self.SendShellCommand("setprop ro.test_harness 1", retry_count=retry_count)
      # manual rest bootcomplete flag
      self.SendShellCommand("setprop dev.bootcomplete 0",
                            retry_count=retry_count)
      self.SendShellCommand("stop", retry_count=retry_count)

    try:
      output = self.SendCommand("sync", retry_count=retry_count)
    except AbortError, e:
      error = e
      output = e.msg
    if "Read-only file system" in output:
      SilentLog(output)
      Log("Remounting read-only filesystem")
      self.SendCommand("remount")
      output = self.SendCommand("sync", retry_count=retry_count)
    elif "No space left on device" in output:
      SilentLog(output)
      Log("Restarting device runtime")
      self.SendShellCommand("stop", retry_count=retry_count)
      output = self.SendCommand("sync", retry_count=retry_count)
      self.SendShellCommand("start", retry_count=retry_count)
    elif error is not None:
      # exception occurred that cannot be recovered from
      raise error
    SilentLog(output)
    if runtime_restart:
      # start runtime and wait till boot complete flag is set
      self.SendShellCommand("start", retry_count=retry_count)
      self.WaitForBootComplete()
      # press the MENU key, this will disable key guard if runtime is started
      # with ro.monkey set to 1
      self.SendShellCommand("input keyevent 82", retry_count=retry_count)
    else:
      self.WaitForDevicePm()
    return output

  def GetSerialNumber(self):
    """Returns the serial number of the targeted device."""
    return self.SendCommand("get-serialno").strip()

  def RuntimeReset(self, disable_keyguard=False, retry_count=3, preview_only=False):
    """
    Resets the Android runtime (does *not* reboot the kernel).

    Blocks until the reset is complete and the package manager
    is available.

    Args:
      disable_keyguard: if True, presses the MENU key to disable
        key guard, after reset is finished
      retry_count: number of times to retry reset before failing

    Raises:
      WaitForResponseTimedOutError if package manager does not respond
      AbortError if unrecoverable error occurred
    """

    Log("adb shell stop")
    Log("adb shell start")

    if not preview_only:
      self.SendShellCommand("stop", retry_count=retry_count)
      self.SendShellCommand("start", retry_count=retry_count)

    self.WaitForDevicePm()

    if disable_keyguard:
      Log("input keyevent 82 ## disable keyguard")
      if not preview_only:
        self.SendShellCommand("input keyevent 82", retry_count=retry_count)




"""Simple logging utility. Dumps log messages to stdout, and optionally, to a
log file.

Init(path) must be called to enable logging to a file
"""

import datetime

_LOG_FILE = None
_verbose = False
_log_time = True

def Init(log_file_path):
  """Set the path to the log file"""
  
  global _LOG_FILE
  _LOG_FILE = log_file_path
  print "Using log file: %s" % _LOG_FILE

def GetLogFilePath():
  """Returns the path and name of the Log file"""
  global _LOG_FILE
  return _LOG_FILE

def Log(new_str):
  """Appends new_str to the end of _LOG_FILE and prints it to stdout.

  Args:
    # new_str is a string.
    new_str: 'some message to log'
  """
  msg = _PrependTimeStamp(new_str)
  print msg
  _WriteLog(msg)

def _WriteLog(msg):
  global _LOG_FILE
  if _LOG_FILE is not None:
    file_handle = file(_LOG_FILE, 'a')
    file_handle.write('\n' + str(msg))
    file_handle.close()

def _PrependTimeStamp(log_string):
  """Returns the log_string prepended with current timestamp """
  global _log_time
  if _log_time:
    return "# %s: %s" % (datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"),
        log_string)
  else:
    # timestamp logging disabled
    return log_string  

def SilentLog(new_str):
  """Silently log new_str. Unless verbose mode is enabled, will log new_str
    only to the log file
  Args:
    # new_str is a string.
    new_str: 'some message to log'
  """
  global _verbose
  msg = _PrependTimeStamp(new_str)
  if _verbose:
    print msg
  _WriteLog(msg)

def SetVerbose(new_verbose=True):
  """ Enable or disable verbose logging"""
  global _verbose
  _verbose = new_verbose
  
def SetTimestampLogging(new_timestamp=True):
  """ Enable or disable outputting a timestamp with each log entry"""
  global _log_time
  _log_time = new_timestamp
    
    
    

class MsgException(Exception):
  """Generic exception with an optional string msg."""
  def __init__(self, msg=""):
    self.msg = msg


class WaitForResponseTimedOutError(Exception):
  """We sent a command and had to wait too long for response."""


class DeviceUnresponsiveError(Exception):
  """Device is unresponsive to command."""


class InstrumentationError(Exception):
  """Failed to run instrumentation."""


class AbortError(MsgException):
  """Generic exception that indicates a fatal error has occurred and program
  execution should be aborted."""


class ParseError(MsgException):
  """Raised when xml data to parse has unrecognized format."""