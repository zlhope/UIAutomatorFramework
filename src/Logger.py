import subprocess
import os
import sys
import time
from datetime import datetime
import pickle
import inspect
import adb_interface
#self.module = __import__(str(self.DevName)+'Config')
#importlib.import_module('logger')

def _PrependTimeStamp(log_string):
  """Returns the log_string prepended with current timestamp """
  global _log_time
  if _log_time:
    return "# %s: %s" % (datetime.now().strftime("%m/%d/%y %H:%M:%S"),
        log_string)
  else:
    # timestamp logging disabled
    return log_string  


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
    
class Logger:
    def __init__(self,logName,device_id):
        self.adb = adb_interface.AdbInterface(device_id)
        self.tcCount=0
        self.testPassCount=0
        self.testFailCount=0 
        self.fcCount = 0
        self.anrCount= 0
        self.resetCount=0
        self.anrList=[]
        self.resetList=[]
        self.forceCloseList=[]
        self.tcList=[]
        self.device_id = device_id
        startTime = datetime.now()
        logTime=str(startTime)
        logTime=logTime.split("-")
        logTime="_".join(logTime)
        logTime=logTime.split(":")
        logTime="_".join(logTime)
        self.reportTime=logName+"_"+logTime
        self.startTime = startTime.strftime('%a %b %d %H:%M:%S %Z %Y')
        self.startTimeSeconds=time.time()
        self.screenshotJar=None
        if os.path.exists(os.getcwd()+'/screenshot.jar'):
            self.screenshotJar='"'+os.getcwd()+'/screenshot.jar"'
        elif os.path.exists('C:\\Python27\\screenshot.jar'):
            self.screenshotJar='"C:\\Python27\\screenshot.jar"'

        productName = subprocess.Popen('adb -s ' + self.device_id + ' shell getprop ro.product.device', shell=False,
                                       stdout=subprocess.PIPE).stdout.read().rstrip()
        buildName = subprocess.Popen('adb -s ' + self.device_id + ' shell getprop ro.build.display.id', shell=False,
                                     stdout=subprocess.PIPE).stdout.read().rstrip()
        androidVersion = subprocess.Popen('adb -s ' + self.device_id + ' shell getprop ro.build.version.release', shell=False,
                                     stdout=subprocess.PIPE).stdout.read().rstrip()

        if androidVersion is None or androidVersion == '':
            androidVersion="Device Android version couldn't be fetched"

        if buildName is None or buildName == '':
            buildName = "Build name couldn't be fetched from DUT"
        if productName is not None or productName == '':
            self.logname = productName + "_" + self.device_id + ".html"
            self.lognameTmp= "Tmp_"+productName + "_" + self.device_id + ".html"
            
        else:
            self.logname = device_id + ".html"
            self.lognameTmp= "Tmp_"+device_id + ".html"
            productName = "Product name couldn't be fetched from DUT"

        self.dirName=os.getcwd()+"/Logs/"+self.reportTime
        self.relDirName="./Logs/"+self.reportTime
        if not os.path.exists(self.dirName):
            os.makedirs(self.dirName)
            
        devLog = open(self.dirName + "/" + self.logname, "w")
        
            
        devLog.write("<script type=\"text/javascript\">\n")
        devLog.write("function toggleMe(a){\n")
        devLog.write("var e=document.getElementById(a);\n")
        devLog.write("if(!e)return true;\n")
        devLog.write("if(e.style.display==\"none\"){\n")
        devLog.write("e.style.display=\"block\"\n")
        devLog.write("}\n")
        devLog.write("else{\n")
        devLog.write("e.style.display=\"none\"\n")
        devLog.write("}\n")
        devLog.write("return true;\n")
        devLog.write("}\n")
        devLog.write("</script>\n")
        
        
        devLog.write("<body bgcolor='#e6e6ff'>\n")
        devLog.write("<font color='#300000'><h1><U>Test Report</U></h1></font>\n")
        devLog.write("<h2><U>Script Name</U>: <font color='blue'>" + logName + "</h2></font>\n")
        devLog.write("<h2><U>Product Name</U>: <font color='blue'>" + productName + "</h2></font>\n")
        devLog.write("<h2><U>Build Name</U>: <font color='blue'>" + buildName + "</h2></font>\n")
        devLog.flush()
        devLog.close()
        
        crashLog = open(self.dirName + "/crashLogs.html", "w")
        crashLog.write("<body bgcolor='#e6e6ff'>\n")
        crashLog.write("<font color='#300000'><h1><U>Crash Logs</U></h1></font>\n")
        crashLog.write("<h2><U>Script Name</U>: <font color='blue'>" + logName + "</h2></font>\n")
        crashLog.write("<h2><U>Product Name</U>: <font color='blue'>" + productName + "</h2></font>\n")
        crashLog.write("<h2><U>Build Name</U>: <font color='blue'>" + buildName + "</h2></font>\n")
        crashLog.flush()
        crashLog.close()

        self.reportDetails=[productName,buildName,logName,self.relDirName + "/" + self.logname,self.startTime,androidVersion]
        with open(self.dirName + "/" +'reportDetails','w') as f1:
            pickle.dump(self.reportDetails,f1)

        self.executionSummary=[]
        with open(self.dirName + "/" +'executionSummary','w') as f2:
            pickle.dump(self.executionSummary,f2)

        self.crashSummary=[[],[],[]]
        with open(self.dirName + "/" +'crashSummary','w') as f3:
            pickle.dump(self.crashSummary,f3)

        
    def waitForDevice(self):
        try:
            if not self.adb.WaitForBootComplete():
                print "found reset"
                self.logReset()
                return False
            return True

        except Exception, e:
            print e
            return False
        
    def screenshot(self,filepath):
        try:
            FNULL = open(os.devnull, "w")

            if self.screenshotJar is not None:
                sceenshotCmd = 'java -jar '+self.screenshotJar+' -s ' + self.device_id + ' "' + filepath + ' "'
                print sceenshotCmd
                temp = subprocess.call(sceenshotCmd, stdout=FNULL, stderr=subprocess.STDOUT)
                print "Done capturing screenshot"
            else:
                raise Exception("screenshot.jar couldn't be found in current directory or C:\\Python27")
        except Exception, e:
            print e


    def headerLog(self, msg, info):
        self.headerLogFlag=True
        if not isinstance(msg, str):
            msg=str(msg)
            
        if not isinstance(info, str):
            info=str(info)
        self.tcCount+=1
        tc=TestCase()
        
        tc.setTcName(msg)
        tc.setTcInfo(info)
        self.tcList.append(tc)
            
        self.f=open(self.dirName + "/" + self.lognameTmp, "a")
        
        self.f.write("<table border='1' cellpadding='10'>\n")
        self.f.write("<tr style='background-color:#66b3ff;'>\n")
        self.f.write('<td><b><font color=#000000>TEST CASE NAME: </font></b></td>\n')
        self.f.write('<td><b><font color=#000000><a name="'+msg+'">'+msg+'</a></font></b></td>\n')        
        self.f.write("</tr>\n")
        self.f.write("<tr style='background-color:#66b3ff;'>\n")
        self.f.write('<td><b><font color=#000000>START TIME: </font></b></td>\n')
        self.headerTime = time.time()
        self.f.write('<td><font color=#000000><b>'+str(datetime.now())+'</b></font></td>\n')
        self.f.write("</tr>\n")
        self.f.write("<tr style='background-color:#66b3ff;'>\n")
        self.f.write('<td><b><font color=#000000>TEST CASE INFO: </font></b></td>\n')        
        self.f.write('<td><b><font color=#000000>'+info+'</font></b></td>\n')        
        self.f.write("</tr>\n")
        self.f.write("</table>\n")        
        
        self.f.write("<br>\n")        
        self.f.write("<input type=\"button\" onclick=\"return toggleMe('para"+str(self.tcCount)+"')\" value=\"Script Logs\"><br>  \n")    
        self.f.write("<div id=\"para"+str(self.tcCount)+"\" style=\"display: none;\">\n")  
        self.f.flush()

        summary=[msg,info,None,'Under Execution']
        self.executionSummary.append(summary)
        with open(self.dirName + "/" +'executionSummary','w') as f2:
            pickle.dump(self.executionSummary,f2)
        
  
    
    def setupError(self, msg):
        f=open(self.dirName+"/setupError.txt",'w')
        f.write(str(msg))
        f.flush()
        f.close()
    
    
    def log(self, msg, logType="I", screenshotName = None):
        try:            
            if not isinstance(msg, str):
                msg=str(msg)
            #If message type is "Debug"
            if logType=="D":
                self.waitForDevice()
                msg="["+str(datetime.now())+"] "+ msg    
                msg="<p><font color='green'>"+msg+"</font></p>\n"
                self.f.write(msg)        
                self.f.flush()
            #If message type is "Error"
            elif logType=="E":
                self.waitForDevice()
                if screenshotName is not None:
                    filename=self.dirName+'/'+screenshotName+'.png'
                    self.screenshot(filename)
                    msg="["+str(datetime.now())+"] "+ msg
                    msg="<p><b><font color='red'>"+msg+"</font></b></p><a href=\""+'./'+screenshotName+".png\"><b>Screenshot</b ></a>\n"
                else:
                    msg="["+str(datetime.now())+"] "+ msg
                    msg="<p><b><font color='red'>"+msg+"</font></b></p>\n"
                self.f.write(msg)        
                self.f.flush()
            #If message type is "Info"    
            elif logType=="I":    
                self.waitForDevice()            
                msg="["+str(datetime.now())+"] "+ msg    
                msg="<p>"+msg+"</p>"
                self.f.write(msg)        
                self.f.flush()                
            else:
                self.waitForDevice()
                raise Exception("Unknown Log Type: %s" %logType)
                
        except Exception, e:
            msg="["+str(datetime.now())+"] "+ msg    
            msg="<p><font color='red'>"+str(e)+"</font></p>\n"
            self.f.write(msg)        
            self.f.flush()


    def logPass(self, repetitionCount=None, passRepetitionCount=None):
        print "Test Case Passed"
        self.tcList[len(self.tcList)-1].setTcResult("PASS")
        if repetitionCount is not None:
            self.tcList[len(self.tcList)-1].setRepetitionCount(str(repetitionCount))
        if passRepetitionCount is not None:
            self.tcList[len(self.tcList)-1].setPassRepetitionCount(str(passRepetitionCount))
        self.testPassCount=self.testPassCount+1
        self.f.write('</div> \n')
        self.f.write("<p>Result: "+'<b><font size="+1" color="green">PASS</font></b></p>\n')
        if self.headerLogFlag:
            self.f.write("<p>Execution Time (in Minutes): <b>"+str("{0:.2f}".format((time.time()-self.headerTime)/60))
                         +"<b></p>\n")
            #summary=[msg,info,None,'executing']
            self.executionSummary[len(self.executionSummary)-1][2]=str("{0:.2f}".format((time.time()-self.headerTime)/60))
            self.executionSummary[len(self.executionSummary)-1][3]='Pass'
            with open(self.dirName + "/" +'executionSummary','w') as f2:
                pickle.dump(self.executionSummary,f2)
            self.headerLogFlag=False
        filename=self.dirName+'/'+self.tcList[len(self.tcList)-1].getTcName()+'.png'
        self.screenshot(filename)
        self.f.write('<b><font color="green"><a href="'+'./'+self.tcList[len(self.tcList)-1].getTcName()+'.png'+
                     '">Screenshot</a></font></b><br><hr><br>\n')

             

    def logFail(self, repetitionCount=None, passRepetitionCount=None):
        print "Test Case Failed"
        self.tcList[len(self.tcList)-1].setTcResult("FAIL")
        if repetitionCount is not None:
            self.tcList[len(self.tcList)-1].setRepetitionCount(str(repetitionCount))
        if passRepetitionCount is not None:
            self.tcList[len(self.tcList)-1].setPassRepetitionCount(str(passRepetitionCount))
        self.testFailCount=self.testFailCount+1
        self.f.write('</div> \n')
        self.f.write("<p>Result: "+'<b><font size="+1" color="red">FAIL</font></b></p>\n')
        if self.headerLogFlag:
            self.f.write("<p>Execution Time (in Minutes): <b>"+str("{0:.2f}".format((time.time()-self.headerTime)/60))
                         +"<b></p>\n")
            #summary=[msg,info,None,'executing']
            self.executionSummary[len(self.executionSummary)-1][2]=str("{0:.2f}".format((time.time()-self.headerTime)/60))
            self.executionSummary[len(self.executionSummary)-1][3]='Fail'
            with open(self.dirName + "/" +'executionSummary','w') as f2:
                pickle.dump(self.executionSummary,f2)
            self.headerLogFlag=False
        filename=self.dirName+'/'+self.tcList[len(self.tcList)-1].getTcName()+'.png'
        self.screenshot(filename)
        self.f.write('<b><font color="red"><a href="'+'./'+self.tcList[len(self.tcList)-1].getTcName()+'.png'+'">Screenshot</a></font></b><br><hr><br>\n')
        
        


    def closeLog(self):
        try:
            self.f.flush()
            self.f.close()
        except Exception, e:
            print e
        
        crashFlag=False
        
        stopTime = datetime.now()
        stopTime = stopTime.strftime('%a %b %d %H:%M:%S %Z %Y')
        
        devLog = open(self.dirName + "/" + self.logname, "a")
        devLog.write("<table border='1' cellpadding='10'>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Total Number of Test Cases: </b></th>\n")
        devLog.write("<th><b>" + str(self.tcCount) + "</b></th>\n")
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Number of Passed Test Cases: </b></th>\n")
        devLog.write("<th><b>" + str(self.testPassCount) + "</b></th>\n")
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Number of Failed Test Cases: </b></th>\n")
        devLog.write("<th><b>" + str(self.testFailCount) + "</b></th>\n")
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Number of ANR Found: </b></th>\n")
        if self.anrCount!=0:
            crashFlag=True
            devLog.write("<th><b><big><big><a href=./CrashLogs.html>" + str(self.anrCount) + "</a></big></big></b></th>\n")
        else:
            devLog.write("<th><b>" + str(self.anrCount) + "</b></th>\n")
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Number of Force Close Found: </b></th>\n")
        if self.fcCount!=0:
            crashFlag=True
            devLog.write("<th><b><big><big><a href=./CrashLogs.html>" + str(self.fcCount) + "</a></big></big></b></th>\n")
        else:
            devLog.write("<th><b>" + str(self.fcCount) + "</b></th>\n")
            
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Number of Reboot Found: </b></th>\n")
        if self.resetCount!=0:
            crashFlag=True
            devLog.write("<th><b><big><big><a href=./CrashLogs.html>" + str(self.resetCount) + "</a></big></big></b></th>\n")
        else:
            devLog.write("<th><b>" + str(self.resetCount) + "</b></th>\n")
            
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Execution Start Time: </b></th>\n")
        devLog.write("<th><b>" + str(self.startTime) + "</b></th>\n")
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Execution End Time: </b></th>\n")
        devLog.write("<th><b>" + str(stopTime) + "</b></th>\n")
        devLog.write("</tr>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Total Execution Time (In Minutes): </b></th>\n")
        devLog.write("<th><b>" + str("{0:.2f}".format((time.time()-self.startTimeSeconds)/60)) + "</b></th>\n")
        devLog.write("</tr>\n")
        
        devLog.write("</table>\n")
        devLog.write("<br>\n")
        devLog.write("<table border='1' cellpadding='10'>\n")
        devLog.write("<tr>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Test Case id</font></b></th>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Description</font></b></th>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Iteration</font></b></th>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Passed Iteration</font></b></th>\n")
        devLog.write("<th bgcolor='#003366'><b><font color='#FFFFFF'>Result</font></b></th>\n")
        devLog.write("</tr>\n")
        for i in range(len(self.tcList)):
            devLog.write("<tr>")
            devLog.write("<th><b>"+str(self.tcList[i].getTcName())+"</b></th>\n")
            devLog.write("<th><b>"+str(self.tcList[i].getTcInfo())+"</b></th>\n")
            devLog.write("<th><b>"+str(self.tcList[i].getRepetitionCount())+"</b></th>\n")
            devLog.write("<th><b>"+str(self.tcList[i].getPassRepetitionCount())+"</b></th>\n")
            devLog.write("<th><b><a href=\"#"+str(self.tcList[i].getTcName())+"\">"+str(self.tcList[i].getTcResult())+"</a></b></th>\n")
            devLog.write("</tr>\n")
        devLog.write("</table>\n")
        devLog.write("<br><hr><br>\n")
        self.f=open(self.dirName + "/" + self.lognameTmp, "r")
        devLog.write(self.f.read())
        
        devLog.flush()
        devLog.close()
        self.f.flush()
        self.f.close()
        
        
        try:
            os.remove(self.dirName + "/" + self.lognameTmp)
        except Exception,e:
            print str(e)

        if crashFlag==True:
        
            crashLog = open(self.dirName + "/CrashLogs.html", "a")
            
            crashLog.write("<table border='1' cellpadding='10'>\n")
            crashLog.write("<tr>\n")
            crashLog.write("<th>\n")
            
            crashLog.write("<table border='1' cellpadding='10'>\n")
            crashLog.write("<tr>\n")
            crashLog.write("<th bgcolor='#003366' colspan='4' ><b><font color='#FFFFFF'>Reboot Summary</font></b></th>\n")
            crashLog.write("</tr>\n")
            
            if self.resetCount!=0:
                crashLog.write("<tr>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Test Case id</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Log Path</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Occurence Time</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Hours for failure</font></b></th>\n")
                crashLog.write("</tr>\n")
                for i in range(len(self.resetList)):
                    crashLog.write("<tr>")
                    crashLog.write("<th><b>"+str(self.resetList[i].getTcName())+"</b></th>\n")
                    crashLog.write("<th><b><a href=\""+str(self.resetList[i].getPath())+"\">link</a></b></th>\n")
                    crashLog.write("<th><b>"+str(self.resetList[i].getOccurenceTime())+"</b></th>\n")
                    crashLog.write("<th><b>"+str(self.resetList[i].getTimeToFailure())+"</b></th>\n")

                    crashLog.write("</tr>\n")
            else:
                crashLog.write("<tr>\n")
                crashLog.write("<th bgcolor='#3399ff' colspan='3' ><b><font color='#FFFFFF'>No reboot observed.</font></b></th>\n")
                crashLog.write("</tr>\n")
                
            crashLog.write("</table>\n")
            
            crashLog.write("</th>\n")
            
            #####################################
            crashLog.write("<th>\n")
            crashLog.write("<table border='1' cellpadding='10'>\n")
            crashLog.write("<tr>\n")
            crashLog.write("<th bgcolor='#003366' colspan='5' ><b><font color='#FFFFFF'>Force Close Summary</font></b></th>\n")
            crashLog.write("</tr>\n")
            if self.fcCount!=0:
                crashLog.write("<tr>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Test Case id</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Crashed App</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Log Path</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Occurence Time</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Hours for failure</font></b></th>\n")
                crashLog.write("</tr>\n")
                for i in range(len(self.forceCloseList)):
                    crashLog.write("<tr>")
                    crashLog.write("<th><b>"+str(self.forceCloseList[i].getTcName())+"</b></th>\n")
                    crashLog.write("<th><b>"+str(self.forceCloseList[i].getCrashedApp())+"</b></th>\n")
                    crashLog.write("<th><b><a href=\""+str(self.forceCloseList[i].getPath())+"\">link</a></b></th>\n")
                    crashLog.write("<th><b>"+str(self.forceCloseList[i].getOccurenceTime())+"</b></th>\n")
                    crashLog.write("<th><b>"+str(self.forceCloseList[i].getTimeToFailure())+"</b></th>\n")
                    crashLog.write("</tr>\n")
            else:
                crashLog.write("<tr>\n")
                crashLog.write("<th bgcolor='#3399ff' colspan='4' ><b><font color='#FFFFFF'>No Force close observed.</font></b></th>\n")
                crashLog.write("</tr>\n")
            crashLog.write("</table>\n")
            crashLog.write("</th>\n")
            
            
            #####################################
            crashLog.write("<th>\n")
            crashLog.write("<table border='1' cellpadding='10'>\n")
            crashLog.write("<tr>\n")
            crashLog.write("<th bgcolor='#003366' colspan='4' ><b><font color='#FFFFFF'>ANR Summary</font></b></th>\n")
            crashLog.write("</tr>\n")
            
            if self.anrCount!=0:
                crashLog.write("<tr>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Test Case id</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Log Path</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Occurence Time</font></b></th>\n")
                crashLog.write("<th bgcolor='#3399ff'><b><font color='#FFFFFF'>Hours for failure</font></b></th>\n")
                crashLog.write("</tr>\n")
                for i in range(len(self.anrList)):
                    crashLog.write("<tr>")
                    crashLog.write("<th><b>"+str(self.anrList[i].getTcName())+"</b></th>\n")
                    crashLog.write("<th><b><a href=\""+str(self.anrList[i].getPath())+"\">link</a></b></th>\n")
                    crashLog.write("<th><b>"+str(self.anrList[i].getOccurenceTime())+"</b></th>\n")
                    crashLog.write("<th><b>"+str(self.anrList[i].getTimeToFailure())+"</b></th>\n")
                    crashLog.write("</tr>\n")
            else:
                crashLog.write("<tr>\n")
                crashLog.write("<th bgcolor='#3399ff' colspan='3' ><b><font color='#FFFFFF'>No ANR observed.</font></b></th>\n")
                crashLog.write("</tr>\n")
                
                
            crashLog.write("</table>\n")
            crashLog.write("</th>\n")
            
            crashLog.write("</tr>\n")
            crashLog.write("</table>\n")
            
            crashLog.flush()
            crashLog.close()
        else:
            try:
                os.remove(self.dirName + "/CrashLogs.html")
            except Exception,e:
                print str(e)
            
            


    def logForceClose(self, fcMsg=None):
        
        fc=FC()
        if len(self.tcList)!=0:
            fc.setTcName(self.tcList[len(self.tcList)-1].getTcName())
        else:
            fc.setTcName('NA')

        OccurenceTime=str(datetime.now())
        print OccurenceTime
        fc.setOccurenceTime(str(datetime.now()))
        print fc.getOccurenceTime()
        print fcMsg

        fc.setTimeToFailure(str("{0:.2f}".format((time.time()-self.startTimeSeconds)/3600)))
        print fc.getTimeToFailure()
        

        self.fcCount +=1
        startTime = datetime.now()
        logTime=str(startTime)
        logTime=logTime.split("-")
        logTime="_".join(logTime)
        logTime=logTime.split(":")
        logTime="_".join(logTime)
        FNULL = open(os.devnull, "w")
        if fcMsg is not None and 'Unfortunately,' in fcMsg:
            fcMsg=fcMsg.split()[1]
            dirName=self.dirName+"/ForceClose/" +fcMsg+'_'+logTime
            dirRelName="./ForceClose/" +fcMsg+'_'+logTime
            fc.setCrashedApp(fcMsg)
            print fc.getCrashedApp()
        else:
            dirName=self.dirName+"/ForceClose/" +logTime
            dirRelName="./ForceClose/" +logTime
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        try:
            sceenshotCmd = 'java -jar '+self.screenshotJar+' -s ' + self.device_id + ' "' + dirName + '/Screenshot.png"'
            print sceenshotCmd
            temp = subprocess.call(sceenshotCmd, stdout=FNULL, stderr=subprocess.STDOUT)
            print "Done capturing screenshot"
        except Exception, e:
            print e

        forceCloseFile = open(dirName + "/logcat.txt", "w")

        forceCloseFile.write(subprocess.Popen('adb -s ' + self.device_id + ' wait-for-device logcat -d -v time',
                                                      shell=False, stdout=subprocess.PIPE).stdout.read())
        forceCloseFile.flush()
        forceCloseFile.close()
        print "Done capturing logcat"
        time.sleep(1)
        bugReportFile = open(dirName + "/bugreport.txt", "wb")
        bugReportFile.write(subprocess.Popen('adb -s ' + self.device_id + ' wait-for-device bugreport', shell=False,
                                                     stdout=subprocess.PIPE).stdout.read())
        bugReportFile.flush()
        bugReportFile.close()
        
        fc.setPath(dirRelName)
        self.forceCloseList.append(fc)
        self.crashSummary[2].append([fc.getTcName(),fc.getTimeToFailure(),fc.getCrashedApp(),fc.getPath()])
        #self.crashSummary=[self.anrList,self.resetList,self.forceCloseList]
        with open(self.dirName + "/" +'crashSummary','w') as f3:
            pickle.dump(self.crashSummary,f3)

        print "Done capturing Bugreport"
        print "logged FC"


    def logReset(self):
        
        reset=Reset()
        if len(self.tcList)!=0:
            reset.setTcName(self.tcList[len(self.tcList)-1].getTcName())
        else:
            reset.setTcName('NA')
            
        reset.setOccurenceTime(str(datetime.now()))
        print "this is time:::::::"
        print str("{0:.2f}".format((time.time()-self.startTimeSeconds)/3600))
        reset.setTimeToFailure(str("{0:.2f}".format((time.time()-self.startTimeSeconds)/3600)))
        print reset.getTimeToFailure()
        
        print "found reset"
        self.resetCount +=1
        startTime = datetime.now()
        logTime=str(startTime)
        logTime=logTime.split("-")
        logTime="_".join(logTime)
        logTime=logTime.split(":")
        logTime="_".join(logTime)
        FNULL = open(os.devnull, "w")
        dirName=self.dirName+"/Reset/" + logTime
        dirRelName="./Reset/" + logTime
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        resetLogcat = open(dirName + "/logcat.txt", "w")

        resetLogcat.write(subprocess.Popen('adb -s ' + self.device_id + ' wait-for-device logcat -d -v time',
                                                      shell=False, stdout=subprocess.PIPE).stdout.read())
        resetLogcat.flush()
        resetLogcat.close()
        print "Done capturing logcat"
        time.sleep(1)
        try:
            sceenshotCmd = 'java -jar '+self.screenshotJar+' -s ' + self.device_id + ' "' + dirName + '/Screenshot.png"'
            print sceenshotCmd
            temp = subprocess.call(sceenshotCmd, stdout=FNULL, stderr=subprocess.STDOUT)
            print "Done capturing screenshot"
        except Exception, e:
            print e
        bugReportFile = open(dirName + "/bugreport.txt", "wb")
        bugReportFile.write(subprocess.Popen('adb -s ' + self.device_id + ' wait-for-device bugreport', shell=False,
                                                     stdout=subprocess.PIPE).stdout.read())
        bugReportFile.flush()
        bugReportFile.close()
        
        reset.setPath(dirRelName)
        self.resetList.append(reset)
        self.crashSummary[1].append([reset.getTcName(),reset.getTimeToFailure(),reset.getPath()])
        #self.crashSummary=[self.anrList,self.resetList,self.forceCloseList]
        with open(self.dirName + "/" +'crashSummary','w') as f3:
            pickle.dump(self.crashSummary,f3)
        
        print "Done capturing Bugreport"
        print "logged Reset"


    def logANR(self):
        
        anr=ANR()
        if len(self.tcList)!=0:
            anr.setTcName(self.tcList[len(self.tcList)-1].getTcName())
        else:
            anr.setTcName('NA')
            
        anr.setOccurenceTime(str(datetime.now()))

        anr.setTimeToFailure(str("{0:.2f}".format((time.time()-self.startTimeSeconds)/3600)))
        print anr.getTimeToFailure()

        
        self.anrCount +=1
        startTime = datetime.now()
        logTime=str(startTime)
        logTime=logTime.split("-")
        logTime="_".join(logTime)
        logTime=logTime.split(":")
        logTime="_".join(logTime)
        FNULL = open(os.devnull, "w")
        dirName=self.dirName+"/ANR/" + logTime
        dirRelName="./ANR/" + logTime
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        try:
            sceenshotCmd = 'java -jar '+self.screenshotJar+' -s ' + self.device_id + ' "' + dirName + '/Screenshot.png"'
            print sceenshotCmd
            temp = subprocess.call(sceenshotCmd, stdout=FNULL, stderr=subprocess.STDOUT)
            print "Done capturing screenshot"
        except Exception, e:
            print e

        anrFile = open(dirName + "/logcat.txt", "w")

        anrFile.write(subprocess.Popen('adb -s ' + self.device_id + ' wait-for-device logcat -d -v time',
                                                      shell=False, stdout=subprocess.PIPE).stdout.read())
        anrFile.flush()
        anrFile.close()
        print "Done capturing logcat"
        time.sleep(1)
        bugReportFile = open(dirName + "/bugreport.txt", "wb")
        bugReportFile.write(subprocess.Popen('adb -s ' + self.device_id + ' wait-for-device bugreport', shell=False,
                                                     stdout=subprocess.PIPE).stdout.read())
        bugReportFile.flush()
        bugReportFile.close()
        
        anr.setPath(dirRelName)
        self.anrList.append(anr)

        self.crashSummary[0].append([anr.getTcName(),anr.getTimeToFailure(),anr.getPath()])
        with open(self.dirName + "/" +'crashSummary','w') as f3:
            pickle.dump(self.crashSummary,f3)
        
        print "Done capturing Bugreport"
        print "logged ANR"
        
        
class TestCase():
    def __init__(self):
        self.tcName=None
        self.tcInfo=None
        self.tcResult=None
        self.repetitionCount=None
        self.passRepetitionCount=None
    
    def setTcName(self, name):
        self.tcName=name

    def getTcName(self):
        return self.tcName
    
    def setTcInfo(self, info):
        self.tcInfo=info
        
    def getTcInfo(self):
        return self.tcInfo
    
    def setTcResult(self, result):
        self.tcResult=result

    def getTcResult(self):
        return self.tcResult
    
    def setRepetitionCount(self,repetitionCount):
        self.repetitionCount= repetitionCount    
    
    def getRepetitionCount(self):
        if self.repetitionCount is None:
            self.repetitionCount='NA'
        return self.repetitionCount
    
    def setPassRepetitionCount(self,passRepetitionCount):
        self.passRepetitionCount= passRepetitionCount    
    
    def getPassRepetitionCount(self):
        if self.passRepetitionCount is None:
            self.passRepetitionCount='NA'
        return self.passRepetitionCount
    
    
class ANR():
    def __init__(self):
        self.tcName=None
        self.occurenceTime=None
        self.path=None
        self.failureTime=None
    
    def setTcName(self, name):
        self.tcName=name

    def getTcName(self):
        return self.tcName
    
    def setOccurenceTime(self, occurenceTime):
        self.occurenceTime=occurenceTime
        
    def getOccurenceTime(self):
        return self.occurenceTime

    def setTimeToFailure(self,failureTime):
        self.failureTime=failureTime

    def getTimeToFailure(self):
        return self.failureTime
    
    def setPath(self, path):
        self.path=path

    def getPath(self):
        return self.path
    
    
class FC():
    def __init__(self):
        self.tcName=None
        self.occurenceTime=None
        self.crashedApp=None
        self.path=None
        self.failureTime=None
    
    def setTcName(self, name):
        self.tcName=name

    def getTcName(self):
        return self.tcName
    
    
    def setCrashedApp(self, app):
        
        self.crashedApp=app
        print self.crashedApp

    def getCrashedApp(self):
        if self.crashedApp is None:
            self.crashedApp='NA'
        print self.crashedApp
        return self.crashedApp
    
    def setOccurenceTime(self, occurence):
        self.occurenceTime=occurence
        
    def getOccurenceTime(self):
        return self.occurenceTime

    def setTimeToFailure(self,failureTime):
        print failureTime
        self.failureTime=failureTime
        print "self.failureTime is", self.failureTime

    def getTimeToFailure(self):

        return self.failureTime
    
    def setPath(self, path):
        self.path=path

    def getPath(self):
        return self.path
    
    
class Reset():
    def __init__(self):
        self.tcName=None
        self.occurenceTime=None
        #self.failureTime=None
        self.path=None
    
    def setTcName(self, name):
        self.tcName=name

    def getTcName(self):
        return self.tcName
    
    def setOccurenceTime(self, occurenceTime):
        self.occurenceTime=occurenceTime
        
    def getOccurenceTime(self):
        return self.occurenceTime

    def setTimeToFailure(self,failureTime):
        print failureTime
        self.failureTime=failureTime
        print "self.failureTime is", self.failureTime

    def getTimeToFailure(self):
        print self.failureTime
        return self.failureTime

    def setPath(self, path):
        self.path=path

    def getPath(self):
        return self.path