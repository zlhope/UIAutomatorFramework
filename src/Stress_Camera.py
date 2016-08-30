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
logger=Logger.Logger('Stress_Camera',deviceId)


class Stress_Camera(unittest.TestCase):
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
            self.camera = UnitModule.Camera(self.input,deviceId,logger)
         
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
# Objective:	Take 1000 pictures and video from camera
# TPS Reference: NA
# Description: 1.Launch Camera App
#              2.take picture
#              3.take video
#              3.Delete picture
# No of loops:  1000
#********************************************************************************************
    def test_001_take1000PicturesVideos(self, iteration=1000):
        try:
            print('test_001:Take 1000 pictures and video from camera ')
            logger.headerLog('test_001', 'Take 1000 pictures and video from camera')

            failCount=0

            for i in range(iteration):
                try:
                    logger.log("Begin iteration:"+str(i+1))
                    print "Begin iteration:"+str(i+1)
                    time.sleep(1)
                    if i%10==0:
                        print "in if"
                        self.input.press.back()
                        self.input.press.back()
                        self.input.press.home()
                        self.camera.deleteCameraImageVideos()
                        self.input.wait.update()
                        if not self.camera.takePicture():
                            raise Exception("Unable to take picture no."+str(i+1))
                        self.input.wait.update()
                        time.sleep(2)
                        logger.log("Took picture no."+str(i+1))
                        if not (GlobalConfig.MasterModel in ["falcon","Ironman","TC75","TC70","TC700H"]):
                            logger.log("self.input.swipe(self.unit.devWidth/3, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10)",'D')
                            self.input.swipe(self.unit.devWidth/3, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10)
                            self.input.wait.update()
                            time.sleep(1)
                            #tap on Camera Switcher
                            if not self.unit.tapOn(uiText=Config.SwtchToVideo['text']):
                                raise Exception("Unable to tap on SwtchToVideo")
                            self.input.wait.update()
                            time.sleep(2)
                            if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                                raise Exception("Unable to tap on Shutter")
                            self.input.wait.update()
                            time.sleep(30)
                            #tap on CameraShutter to stop video recording
                            if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                                raise Exception("Unable to tap on Shutter")
                            self.input.wait.update()
                            time.sleep(1)


                        else:
                            if not self.unit.tapOn(uiId=Config.CameraSwitcher['id']):
                                raise Exception("Unable to tap on Camera Switcher")
                            self.input.wait.update()
                            #tap on SwtchToVideo
                            if not self.unit.tapOn(uiDescription=Config.SwtchToVideo['description']):
                                raise Exception("Unable to switch to Photo")
                            self.input.wait.update()
                            time.sleep(2)
                            if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                                raise Exception("Unable to tap on Shutter")
                            self.input.wait.update()
                            time.sleep(30)
                            #tap on CameraShutter to stop video recording
                            if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                                raise Exception("Unable to tap on Shutter")
                            self.input.wait.update()
                            time.sleep(1)

                        logger.log("Took video no."+str(i+1))

                    else:
                        time.sleep(2)

                        if not (GlobalConfig.MasterModel in ["falcon","Ironman","TC75","TC70","TC700H"]):

                            logger.log("self.input.swipe(self.unit.devWidth/3, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10)",'D')
                            self.input.swipe(self.unit.devWidth/3, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10)
                            self.input.wait.update()
                            time.sleep(1)
                            if not self.unit.tapOn(uiText=Config.SwtchToPhoto['text']):
                                raise Exception("Unable to tap on SwtchToPhoto")
                            self.input.wait.update()
                            time.sleep(2)
                        else:
                            if not self.unit.tapOn(uiId=Config.CameraSwitcher['id']):
                                raise Exception("Unable to tap on Camera Switcher")
                            self.input.wait.update()
                            if not self.unit.tapOn(uiDescription=Config.SwtchToPhoto['description']):
                                raise Exception("Unable to tap on SwtchToPhoto")
                            self.input.wait.update()
                            time.sleep(2)


                        #tap on Camera Switcher

                        if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                            raise Exception("Unable to take picture no."+str(i+1))
                        self.input.wait.update()
                        logger.log("Took picture no."+str(i+1))
                        time.sleep(2)
                        if not (GlobalConfig.MasterModel=='falcon' or GlobalConfig.MasterModel=='Ironman'):
                            logger.log("self.input.swipe(self.unit.devWidth/3, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10)",'D')
                            self.input.swipe(self.unit.devWidth/3, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10)
                            self.input.wait.update()
                            time.sleep(1)
                            if not self.unit.tapOn(uiText=Config.SwtchToVideo['text']):
                                raise Exception("Unable to tap on SwtchToVideo")
                            self.input.wait.update()
                            time.sleep(2)
                        else:
                            if not self.unit.tapOn(uiId=Config.CameraSwitcher['id']):
                                raise Exception("Unable to tap on Camera Switcher")
                            self.input.wait.update()
                        #tap on Camera Switcher
                            if not self.unit.tapOn(uiDescription=Config.SwtchToVideo['description']):
                                raise Exception("Unable to switch to Photo")
                            self.input.wait.update()
                            time.sleep(2)

                        if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                            raise Exception("Unable to tap on Shutter")
                        self.input.wait.update()
                        time.sleep(30)
                        #tap on CameraShutter to stop video recording
                        if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                            raise Exception("Unable to tap on Shutter")
                        self.input.wait.update()
                        time.sleep(2)
                        logger.log("Took video no."+str(i+1))



                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_001_take1000PicturesVideos_'+str(i+1))



            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:

                print failCount
                raise Exception("Couldn't capture picture/video for "+str(failCount)+" times")


        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail(iteration,iteration-failCount)


        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)



#********************************************************************************************
# Objective:	Take 1000 pictures from camera
# TPS Reference: NA
# Description: 1.Launch Camera App
#              2.take picture 
#              3.Delete picture
# No of loops:  1000
#********************************************************************************************
    def test_002_take1000Pictures(self, iteration=1000):
        try:
            print('test_002:take 1000 pictures from camera ')
            logger.headerLog('test_002', 'take 1000 pictures from camera')
            
            failCount=0

            for i in range(iteration):
                try:
                    logger.log("Begin iteration:"+str(i+1))
                    print "Begin iteration:"+str(i+1)
                    time.sleep(1)
                    if i%20==0:
                        print "in if"
                        self.input.press.back()
                        self.input.press.back()
                        self.input.press.home()
                        self.camera.deleteCameraImageVideos()
                        self.input.wait.update()
                        if not self.camera.takePicture():
                            raise Exception("Unable to take picture no."+str(i+1))
                        logger.log("Took picture no."+str(i+1))
                        self.input.wait.update()
                    else:
                        time.sleep(2)
                        if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                            raise Exception("Unable to take picture no."+str(i+1))
                        self.input.wait.update()
                        logger.log("Took picture no."+str(i+1))
                        
                    

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_002_take1000Pictures_'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't capture picture for "+str(failCount)+" times")
                

        except Exception, e:
            logger.log(str(e),'E')
            logger.logFail(iteration,iteration-failCount)
            
            
        except KeyboardInterrupt:
            logger.log("Test cancelled by User",'E')
            logger.logFail()
            logger.closeLog()
            os._exit(1)





#********************************************************************************************
# Objective:	Take 1000 30sec videos from camera
# TPS Reference: NA
# Description: 1.Launch Camera App
#              2.take video for 30sec
#              3.Delete picture
# No of loops:  1000
#********************************************************************************************
    def test_003_take1000Videos(self, iteration=1000):
        try:
            print('test_003:take 1000 30sec videos from camera ')
            logger.headerLog('test_003', 'take 1000 30sec videos from camera ')
            
            failCount=0

            for i in range(iteration):
                try:
                    logger.log("Begin iteration:"+str(i+1))
                    print "Begin iteration:"+str(i+1)
                    time.sleep(1)
                    if i%5==0:
                        self.input.press.back()
                        self.input.press.back()
                        self.input.press.home()
                        self.camera.deleteCameraImageVideos()
                        self.input.wait.update()
                        if not self.camera.takeVideo(30):
                            raise Exception("Unable to take video no."+str(i+1))
                        logger.log("Took video no."+str(i+1))
                        self.input.wait.update()
                    else:
                        if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                            raise Exception("Unable to tap on Shutter to start video capture ")
                        self.input.wait.update()
                        time.sleep(30)
                        
                        if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                            raise Exception("Unable to tap on Shutter to stop video capture ")
                        self.input.wait.update()
                        time.sleep(3)
                        
                        logger.log("Took video no."+str(i+1))
                        
                    

                    logger.log("iteration "+str(i+1)+" passed")

                except Exception,e:
                    failCount+=1
                    logger.log(str(e),'E')
                    logger.log("iteration "+str(i+1)+" failed",'E','test_003_take1000Videos_'+str(i+1))

        
        
            if failCount < iteration*.05:
                logger.logPass(iteration,iteration-failCount)
                print "Test Passed"
            else:
                
                print failCount
                raise Exception("Couldn't capture video for "+str(failCount)+" times")
                

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