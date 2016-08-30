#import all the inbuilt modules
import unittest
import time
import importlib
import sys
import os

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
logger=Logger.Logger('Stress_Browser',deviceId)
OS_version=GlobalConfig.MasterAndroidVersion

class Stress_Browser(unittest.TestCase):
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
            self.wifi = UnitModule.Wifi(self.input,deviceId,logger)
         
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
# Objective: Visit AT&T website

# No of loops:  350
#********************************************************************************************
    def test_001_visitATTWebsite(self, iteration=350):
        try:
            print('test_001: Visit AT&T website')
            logger.headerLog('test_001', 'Visit AT&T website for 1000 times')
            
            failCount=0
            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    if not self.unit.launchApp(Config.Browser['text']):
                        raise Exception("Unable to launch Browser App")
                    logger.log("Launched Browser App")
                    time.sleep(1)
                        
                    if not self.browser.openWebPage("www.att.com",None, False):
                        raise Exception("Unable to open ATT WebPage ")
                    logger.log("Opened ATT webpage")
                    self.input.wait.update()
                    time.sleep(10)

                    self.input.press.back()
                    self.input.press.back()
                    self.input.press.home()
                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_visitATTWebsite'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't Opene ATT page for "+str(failCount)+" times")
                

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail(iteration,iteration-failCount)
            
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)



    def test_002_connectWifi(self, iteration=1):
        try:
            time.sleep(3600)
            print('test_002:Connect to WiFi AP with new password')
            logger.headerLog('test_002', 'Connect to WiFi AP with new password')

            failCount=0
            while(True):
                try:

                    print "Begin iteration:"
                    logger.log("Begin iteration:")
                    time.sleep(1)
                    if not self.wifi.connectToWiFi(GlobalConfig.WifiName, "Access4Guests2016"):
                        raise Exception("Unable to connect to given WiFi")
                    logger.log("Connected to given WiFI AP")
                    self.input.wait.update()

                    if not self.browser.openWebPage("www.google.com",None, True):
                            raise Exception("Unable to open google WebPage ")
                    break


                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration failed",'E','test_002_connectWifi')



            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:

                print failCount
                raise Exception("Couldn't connect to WiFi "+str(failCount)+" times")


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