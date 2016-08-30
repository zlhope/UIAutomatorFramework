#import all the inbuilt modules
import unittest
import time
import os
import importlib
import sys

#import all the user defined modules
import Logger
import GlobalConfig

#import Device class from uiautomator package
from uiautomator import Device
#Serial id of DUT
deviceId= GlobalConfig.MasterDeviceId
#Seerial id of Partner Device
deviceId2= GlobalConfig.SlaveDeviceId
#Dynamically import the specified model folder and files
UnitModule=importlib.import_module(GlobalConfig.MasterModel+'_'+GlobalConfig.MasterAndroidVersion+GlobalConfig.MasterGMSnonGMS)
Config=UnitModule.Config()
logger=Logger.Logger('Sanity_All_MS',deviceId)

#Dynamically import the files of support device
UnitModule2=importlib.import_module(GlobalConfig.SlaveModel+'_'+GlobalConfig.SlaveAndroidVersion+GlobalConfig.SlaveGMSnonGMS)
Config2=UnitModule.Config()


class Sanity_All(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        logger.closeLog()

    def setUp(self):
        try:
            print 'Set Up'
            self.input = Device(deviceId)
            self.unit= UnitModule.Unit(self.input,deviceId,logger)
            
            self.input2 = Device(deviceId2)
            self.unit2 = UnitModule2.Unit(self.input2,deviceId2)
            
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
        
        self.unit2.sendKeyEvent('BACK')
        self.unit2.sendKeyEvent('BACK')
        self.unit2.sendKeyEvent('BACK')
        self.unit2.sendKeyEvent('HOME')
        self.unit2.sendKeyEvent('BACK')

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
            logger.log("launch Settings App")
                
            #this is just to demonstrate control on partner device   
            if not self.unit2.launchApp(Config2.SettingApp['text']):
                raise Exception("Unable to launch Settings App on partner device")
            logger.log("launched Settings App on partner device")
            
            if not self.unit.enableDisableCheckbox(True,Config.BluetoothOption['text'],True,True):
                raise Exception("Unable to turn on Bluetooth")
            logger.log("turned on Bluetooth")
                
            #this is just to demonstrate control on partner device  
            if not self.unit2.enableDisableCheckbox(True,Config2.BluetoothOption['text'],True,True):
                raise Exception("Unable to turn on Bluetooth on partner device")
            logger.log("turned on Bluetooth on partner device")

            self.input.wait.update()
            
            #this is just to demonstrate control on partner device 
            self.input2.wait.update()

            if not self.unit.enableDisableCheckbox(False,Config.BluetoothOption['text'],True,True):
                raise Exception("Unable to turn off Bluetooth")
            logger.log("turned off  Bluetooth")
            
            #this is just to demonstrate control on partner device
            if not self.unit2.enableDisableCheckbox(False,Config2.BluetoothOption['text'],True,True):
                raise Exception("Unable to turn off Bluetooth on partner device")
            logger.log("turned off  Bluetooth on partner device")
            
            self.input.wait.update()
            
            #this is just to demonstrate control on partner device 
            self.input2.wait.update()

            logger.logPass()
            print "Test Passed"

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail()
            print e
        
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
            logger.log("launch Settings App")

            if not self.unit.tapOn(Config.DisplayOptiont['text'],None,None,True):
                raise Exception("Unable to tap on Display")
            logger.log("tapped on Display option")

            if not self.unit.enableDisableCheckbox(True,Config.AutoRotateScreenText['text'],False, False,"R"):
                raise Exception("Unable to check Auto-rotate screen checkbox")
            logger.log("checked Auto-rotate screen checkbox")
            
            self.input.wait.update()

            if not self.unit.enableDisableCheckbox(False,Config.AutoRotateScreenText['text'],False, False,"R"):
                raise Exception("Unable to uncheck Auto-rotate screen")
            logger.log("unchecked Auto-rotate screen checkbox")

            self.input.wait.update()

            logger.logPass()
            print "Test Passed"

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail()
            print e
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)

if __name__=='__main__':
    unittest.main()

#To simulate Force close activity-> adb shell am start -n com.android.contacts/com.android.contacts.activities.ContactEditorActivity