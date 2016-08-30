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

#Dynamically import the specified model folder and files
UnitModule=importlib.import_module(GlobalConfig.MasterModel+'_'+GlobalConfig.MasterAndroidVersion+GlobalConfig.MasterGMSnonGMS)
Config=UnitModule.Config()
logger=Logger.Logger('Stress_Multitasking',deviceId)
OS_version=GlobalConfig.MasterAndroidVersion

class Stress_Multitasking(unittest.TestCase):
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
            self.unit = UnitModule.Unit(self.input,deviceId,logger)
            self.browser = UnitModule.Browser(self.input,deviceId,logger)
         
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
# Objective: Switch from the browser application to each running application
# TPS Reference: NA
# Description: 1.Launch Browser and load a webpage
#              2.Switch to different applications 
# No of loops:  1000
#********************************************************************************************
    def test_001_switchFromBrowser(self, iteration=1000):
        try:
            print('test_001:Switch from the browser application to each running application 1000 times')
            logger.headerLog('test_001', 'Switch from the browser application to each running application 1000 times')
            
            failCount=0
            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    time.sleep(1)
                    
                    self.input.press.back()
                    self.input.press.back()
                    self.input.press.back()
                    self.input.press.home()
                    self.input.press.back()
                    if not self.browser.openWebPage("www.google.com"):
                        raise Exception("Unable to open WebPage")
                    logger.log("started Browser session")
                    self.input.press.home()
                    for j in range(len(Config.AppListMultitasking)):
                        
                        if not self.unit.launchApp(Config.AppListMultitasking[j][0],Config.AppListMultitasking[j][1]):
                            raise Exception("Unable to launch "+Config.AppListMultitasking[j][0] +"App")
                        logger.log("Launched "+Config.AppListMultitasking[j][0] +" App")
                        logger.log("Ignore this failure, this line is meant for Checking Crash in "+Config.AppListMultitasking[j][0] +" App")
                        print "code to check crash"
                        self.unit.tapOn("checking crash")
                        self.input.wait.update()
                        time.sleep(3)
                        self.input.press.back()
                        self.input.press.home()
                        
                        
                    if not self.unit.launchApp(Config.Browser['text']):
                        raise Exception("Unable to launch Browser App")
                    logger.log("Launched Browser App")
                    time.sleep(3)
                    self.input.press.back()
                    self.input.press.back()
                    self.input.press.back()
                    logger.log("Closing Browser Session")
                    self.input.press.home()
                        

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_switchFromBrowser_'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't switchFromBrowser for "+str(failCount)+" times")
                

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail(iteration,iteration-failCount)
            
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)




if __name__=='__main__':
    unittest.main()

#To simulate Force close activity-> adb shell am start -n com.android.contacts/com.android.contacts.activities.ContactEditorActivity