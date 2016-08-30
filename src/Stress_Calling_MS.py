# import all the inbuilt modules
import unittest
import time
import importlib
import sys
import os

# import all the user defined modules
import Logger
import GlobalConfig

# import Device class from uiautomator package
from uiautomator import Device
# Serial id of DUT
deviceId= GlobalConfig.MasterDeviceId
# Serial id of Partner Device
deviceId2= GlobalConfig.SlaveDeviceId
# Dynamically import the specified model folder and files
UnitModule=importlib.import_module(GlobalConfig.MasterModel+'_'+GlobalConfig.MasterAndroidVersion+GlobalConfig.MasterGMSnonGMS)
Config=UnitModule.Config()
logger=Logger.Logger('Stress_Calling_MS',deviceId)

# Dynamically import the files of support device
UnitModule2=importlib.import_module(GlobalConfig.SlaveModel+'_'+GlobalConfig.SlaveAndroidVersion+GlobalConfig.SlaveGMSnonGMS)
Config2=UnitModule2.Config()


class Stress_Calling_MS(unittest.TestCase):
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
            self.phone = UnitModule.Phone(self.input,deviceId,logger)
            
            self.input2 = Device(deviceId2)
            self.unit2 = UnitModule2.Unit(self.input2,deviceId2,logger)
            self.phone2 = UnitModule2.Phone(self.input2,deviceId2,logger)
        except Exception, e:
            print e
            logger.setupError(e)
            os._exit(1)
            

    def tearDown(self):
        try:
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
        except Exception, e:
            print e
            logger.setupError(e)

# ********************************************************************************************
# Objective:	Make 1000 calls to support device from dialer
# TPS Reference: NA
# Description: 1.Launch Phone App
#              2.Dial number of support device
#              3.Answer call at support device
# No of loops:  1000
# ********************************************************************************************
    def test_001_make1000Calls(self, iteration=1000):

        failCount = 0
        try:
            print('test_001: Make 1000 calls to support device from dialer ')
            logger.headerLog('test_001_make100Calls', 'Make 1000 calls to support device from dialer')
            


            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    time.sleep(1)
                    if not self.phone.makeVoiceCall(GlobalConfig.SlavePhoneNumber):
                        raise Exception("Unable to make call")
                    logger.log("Initiated call to partner device")
                    self.input.wait.update()
                    if not self.phone2.answerCall():
                        raise Exception("Unable to answer call")
                    logger.log("Answered call on partner device")

                    time.sleep(10)

                    if not self.phone2.endCall():
                        raise Exception("Unable to end call")
                    logger.log("Ended call on partner device")

                    self.input.wait.update()

                    time.sleep(2)

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_make1000Calls_'+str(i+1))

            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't make call for "+str(failCount)+" times")

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail(iteration,iteration-failCount)
            
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)


# ********************************************************************************************
# Objective:	Recieve 1000 calls
# TPS Reference: NA
# Description: 1.Launch Phone App on support device
#              2.Dial number of master device
#              3.Answer call at master device
# No of loops:  1000
# ********************************************************************************************
    def test_002_recieve100Calls(self, iteration=1000):
        failCount = 0
        try:
            print('test_002: Recieve 1000 calls ')
            logger.headerLog('test_002_recieve100Calls', 'Recieve 1000 calls')

            for i in range(iteration):
                try:
                    logger.log("Begin iteration:"+str(i+1))
                    if not self.phone2.makeVoiceCall(GlobalConfig.MasterPhoneNumber):
                        raise Exception("Unable to make call")
                    logger.log("Initiated call from partner device")
                    self.input.wait.update()
                    if not self.phone.answerCall():
                        raise Exception("Unable to answer call")
                    logger.log("Answered call on master device")

                    time.sleep(10)

                    if not self.phone2.endCall():
                        raise Exception("Unable to end call")
                    logger.log("Ended call on partner device")

                    self.input.wait.update()

                    time.sleep(2)

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_002_recieve100Calls_'+str(i+1))

            if failCount < iteration*.05:
                print failCount
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                print failCount
                raise Exception("Couldn't Recieve call for "+str(failCount)+" times")

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