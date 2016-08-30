#import all the inbuilt modules
import unittest
import time
import os
import importlib
import sys

#import all the user defined modules
import Logger
import GlobalConfig

import inspect

#import Device class from uiautomator package
from uiautomator import Device
#Serial id of DUT
deviceId= GlobalConfig.MasterDeviceId
#Dynamically import the specified model folder and files
UnitModule=importlib.import_module(GlobalConfig.MasterModel+'_'+GlobalConfig.MasterAndroidVersion+GlobalConfig.MasterGMSnonGMS)
Config=UnitModule.Config()

logger=Logger.Logger('Sanity_All',deviceId)


class Sanity_All(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        logger.closeLog()

    def setUp(self):
        print 'Set Up'
        
        try:
            self.input = Device(deviceId)
            self.unit= UnitModule.Unit(self.input,deviceId,logger)
        except Exception, e:
            print e
            logger.setupError(e)
            os._exit(1)

    def tearDown(self):
        print 'Tear Down'
        self.unit.sendKeyEvent('BACK')
        self.unit.sendKeyEvent('BACK')
        self.unit.sendKeyEvent('BACK')
        self.unit.sendKeyEvent('HOME')
        self.unit.sendKeyEvent('BACK')


#********************************************************************************************
# Objective:	Verify the bluetooth can be turn on/off
# TPS Reference: NA
# Description: 1.Launch Settings App
#              2.Enable/Disbale bluetooth switch button
# No of loops:  NA
#********************************************************************************************
    def test_001_turnBluetoothOnOff(self):
        try:
            
            print 'test_001_turnBluetoothOnOff'
            logger.headerLog('test_001_turnBluetoothOnOff', 'Turn On /turn off Bluetooth')
            
            
            if not self.unit.launchApp(Config.SettingApp['text']):
                raise Exception("Unable to launch Settings App")
            logger.log("launched settings app")

            if not self.unit.enableDisableCheckbox(True,Config.BluetoothOption['text'],True,True):
                raise Exception("Unable to turn on Bluetooth")
            logger.log("turned on bluetooth")
            self.input.wait.update()

            if not self.unit.enableDisableCheckbox(False,Config.BluetoothOption['text'],True,True):
                raise Exception("Unable to turn off Bluetooth")
            logger.log("turned off bluetooth")
            
            self.input.wait.update()

            logger.logPass()
            print "Test Passed"

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail()
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)

#********************************************************************************************
# Objective:	Verify the autorotation checkbox can be checked and uncheked
# TPS Reference: NA
# Description: 1.Launch Settings App
#              2.Select Display option
#              2.Check/Uncheck Auto-rotate screen checkbox
# No of loops:  NA
#********************************************************************************************
    def test_002_enableDisableAutorotation(self):
        try:
            
            print 'test_002_enableDisableAutorotation'
            logger.headerLog('test_002_enableDisableAutorotation', 'Turn On /turn off Auto-rotation')
           
            if not self.unit.launchApp(Config.SettingApp['text']):
                raise Exception("Unable to launch Settings App")
            logger.log("launched Settings App")

            if not self.unit.tapOn(Config.DisplayOptiont['text'],None,None,True):
                raise Exception("Unable to tap on Display")
            logger.log("tapped on Display text")
            
            if not self.unit.enableDisableCheckbox(True,Config.AutoRotateScreenText['text'],False, False,"R"):
                raise Exception("Unable to check Auto-rotate screen checkbox")
            logger.log("checked Auto-rotate screen checkbox")

            self.input.wait.update()

            if not self.unit.enableDisableCheckbox(False,Config.AutoRotateScreenText['text'],False, False,"R"):
                raise Exception("Unable to uncheck Auto-rotate screen")
            logger.log("unchecked Auto-rotate screen")
            
            self.input.wait.update()

            logger.logPass()
            print "Test Passed"

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail()
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)

if __name__=='__main__':
    unittest.main()

#To simulate Force close activity-> adb shell am start -n com.android.contacts/com.android.contacts.activities.ContactEditorActivity