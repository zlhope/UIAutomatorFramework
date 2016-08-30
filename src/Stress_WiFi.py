#import all the inbuilt modules
import unittest
import time
import os
import importlib
#import sys

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
logger=Logger.Logger('Stress_WiFi',deviceId)
OS_version=GlobalConfig.MasterAndroidVersion

class Stress_WiFi(unittest.TestCase):
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
# Objective:	Turn On/Off WiFi radios for 1000 times
# TPS Reference: NA
# Description: 1.Launch Setting and open WiFi
#              2.turn on WiFi radio and then turn it off 
# No of loops:  1000
#********************************************************************************************
    def test_001_turnWiFiOnOff(self, iteration=1000):
        try:
            print('test_001:Turn On/Off WiFi radios for 1000 times')
            logger.headerLog('test_001', 'Turn On/Off WiFi radios for 1000 times')
            
            failCount=0
            exceptionFlag= False
            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    time.sleep(1)
                    if i==0 or exceptionFlag==True:

                        if exceptionFlag:
                            exceptionFlag= False

                        self.input.press.back()
                        self.input.press.back()
                        self.input.press.back()
                        self.input.press.home()
                        self.input.press.back()
                        if not self.unit.launchApp(Config.SettingApp['text']):
                            raise Exception("Unable to launch Settings App")
                        self.input.wait.update()
                        if OS_version is "LL" or "MM":
                            #wifiText=unicode(Config.WiFi['text'],"utf-8")
                            #if not self.unit.tapOn(uiText=wifiText,scrollable=True):
                            if not self.unit.tapOn(uiText=Config.WiFi['text'],scrollable=True):
                                raise Exception("Unable to tap on Wifi")
                            logger.log("tapped on Wifi")
                            self.input.wait.update()
                            if self.unit.exists(Config.WiFiOFF['text']):
                                if not self.unit.tapOn(Config.WiFiOFF['text']):
                                    raise Exception("Unable to turn on Wifi")
                                logger.log("turned on Wifi")
                                self.input.wait.update()
                                if not self.unit.tapOn(Config.WiFiON['text']):
                                    raise Exception("Unable to turn off Wifi")
                                logger.log("turned off Wifi")
                                self.input.wait.update()
                            else:
                                if not self.unit.tapOn(Config.WiFiON['text']):
                                    raise Exception("Unable to turn off Wifi")
                                logger.log("turned off Wifi")
                                self.input.wait.update()
                                
                        else:
                            if not self.unit.enableDisableCheckbox(True,Config.WiFi['text'],True,True):
                                raise Exception("Unable to turn on Wifi")
                            logger.log("turned on Wifi")
                            self.input.wait.update()
                        
                            if not self.unit.enableDisableCheckbox(False,Config.WiFi['text'],True,True):
                                raise Exception("Unable to turn off WiFi")
                            logger.log("turned off WiFi")
                    else:
                        
                        if OS_version is "LL" or "MM":
                            
                            if self.unit.exists(Config.WiFiOFF['text']):
                                if not self.unit.tapOn(Config.WiFiOFF['text']):
                                    raise Exception("Unable to turn on Wifi")
                                logger.log("turned on Wifi")
                                self.input.wait.update()
                                if not self.unit.tapOn(Config.WiFiON['text']):
                                    raise Exception("Unable to turn off Wifi")
                                logger.log("turned off Wifi")
                                self.input.wait.update()
                            else:
                                if not self.unit.tapOn(Config.WiFiON['text']):
                                    raise Exception("Unable to turn off Wifi")
                                logger.log("turned off Wifi")
                                self.input.wait.update()
                        
                        else:
                            if not self.unit.enableDisableCheckbox(True,Config.WiFi['text'],True,True):
                                raise Exception("Unable to turn on Wifi")
                            logger.log("turned on Wifi")
                            self.input.wait.update()
                            
                            if not self.unit.enableDisableCheckbox(False,Config.WiFi['text'],True,True):
                                raise Exception("Unable to turn off WiFi")
                            logger.log("turned off WiFi")

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    exceptionFlag=True
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_turnWiFiOnOff_'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't turnOn/Off Wifi for "+str(failCount)+" times")
                

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail(iteration,iteration-failCount)
            
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)




#********************************************************************************************
# Objective:	Connect/Disconnect to WiFi AP for 1000 times
# TPS Reference: NA
# Description: 1.Launch Setting and open WiFi
#              2.turn on WiFi radio connect to given AP 
#              3.Forget the connected AP to disconnect
# No of loops:  10000
#********************************************************************************************
    def test_002_connectDisconnectWifi(self, iteration=1000):
        try:
            print('test_002:Connect/Disconnect to WiFi AP for 1000 times')
            logger.headerLog('test_002', 'Connect/Disconnect to WiFi AP for 1000 times')
            
            failCount=0
            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    time.sleep(1)
                    
                    if not self.wifi.connectToWiFi(GlobalConfig.WifiName, GlobalConfig.WifiPassword):
                        raise Exception("Unable to connect to given WiFi")
                    logger.log("Connected to given WiFI AP")
                    self.input.wait.update()
                    if not self.unit.verifyInternetConnection():
                        raise Exception("Ping Failed to Google.com")
                    if not self.wifi.disconnectToWiFi(GlobalConfig.WifiName):
                        raise Exception("Unable to disconnect to given WiFi")
                    logger.log("Disconnected to given WiFI AP")
                    self.input.wait.update()

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_002_connectDisconnectWifi_'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't connect/disconnect to WiFi "+str(failCount)+" times")
                

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