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
logger=Logger.Logger('Stress_Scanning',deviceId)
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
            self.scanning = UnitModule.Scanning(self.input,deviceId,logger)
         
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
# Objective: Scan Barcode for 10000 times
# TPS Reference: NA
# Description: 1.	Launch DW demo
#              2.	Scan Barcode using DWSoft Scan Btn
#
# No of loops:  1000
#********************************************************************************************
    def test_001_scanBarcode(self, iteration=10000):
        try:
            print('test_001: Scan Barcode for 1000 times')
            logger.headerLog('test_001', 'Scan Barcode for 1000 times')
            
            failCount=0
            failCount=0
            for i in range(iteration):
                try:
                    print "Begin iteration:"+str(i+1)
                    logger.log("Begin iteration:"+str(i+1))
                    time.sleep(1)

                    if i % 20 ==0:
                        self.unit.sendKeyEvent('BACK')
                        self.unit.sendKeyEvent('BACK')
                        if not self.scanning.scanFromDataWedge(True):
                            raise Exception("Barcode couldn't be scanned")
                    else:
                        if not self.scanning.scanFromDataWedge():
                            raise Exception("Barcode couldn't be scanned")

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_scanBarcode_'+str(i+1))



            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:

                print failCount
                raise Exception("Couldn't scanBarcode for "+str(failCount)+" times")


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