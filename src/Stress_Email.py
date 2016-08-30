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
logger=Logger.Logger('Stress_Email',deviceId)
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
            self.email = UnitModule.Email(self.input,deviceId,logger)
         
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
# Objective: Send an email with 100KB attachment
# TPS Reference: NA
# Pre-condition : make sure "Attachment.jpg" is present on DUT
# Description: 1.Launch Email
#              2.Send Email with attachment of 100KB
# No of loops:  1000
#********************************************************************************************
    def test_001_sendEmailWithAttachment(self, iteration=1000):
        try:
            print('test_001:Send 1000 emails with 100KB attachment')
            logger.headerLog('test_001', 'Send 1000 emails with 100KB attachment')
            print 'make sure "Attachment.jpg" is present on DUT'
            failCount=0
            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    time.sleep(1)

                    if i % 50 ==0:
                        self.unit.sendKeyEvent('BACK')
                        self.unit.sendKeyEvent('BACK')
                        if not self.email.sendEmail(GlobalConfig.SlaveEmailID,Config.EmailSubjectLine,Config.EmailBodyLine,"Attachment.jpg",True):
                            raise Exception("Email couldn't be sent")
                    else:
                        if not self.email.sendEmail(GlobalConfig.SlaveEmailID,Config.EmailSubjectLine,Config.EmailBodyLine,"Attachment.jpg"):
                            raise Exception("Email couldn't be sent")

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_sendEmailWithAttachment_'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't sendEmailWithAttachment for "+str(failCount)+" times")
                

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