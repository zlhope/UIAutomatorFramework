# ----------------------------------------------------------------------------------------------------------------------
# Name Of File: TC75_ModuleFunctions.py                                                                                #
# Author: Ashish Kumar                                                                                                 #
# Purpose Of File: contains unit level most widely used functions                                                      #
#                                                                                                                      #
# History:                                                                                                             #
# Date                   Author                  Changes                                                               #
# 10/27/2015             Ashish Kumar            First Version                                                         #
# 11/25/2015             Ashish Kumar            Second Version                                                        #
#----------------------------------------------------------------------------------------------------------------------
import os
import sys
rootDir= '\\'.join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, rootDir)
import unittest
import time
import TC70_LL_Config
import ModuleFunctions
Config=TC70_LL_Config.Config()


class Unit(ModuleFunctions.Unit):
        
# ----------------------------------------------------------------------------------------------------------------------
#   scanhardKey (TC70)
#  
#   DESCRIPTION
#   Function to simulate Scan Keypress
#   Args 1
#   Arg. 1.
#   deviceId - (str) device id of the DUT
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def scanhardKey(self):
        try:
            #key down kernel event for scan button
            #below line for TC55
            #cmd=self.command+" sendevent dev/input/event1 4 4 2;sendevent dev/input/event1 1 528 0;sendevent dev/input/event1 0 0 0;"
            cmd=self.command + " sendevent dev/input/event9 1 311 0;sendevent dev/input/event9 0 0 0;"
            os.system(cmd)
            time.sleep(2)
            #key up kernel event for scan button
            #below line for TC55
            #cmd=self.command+" sendevent dev/input/event1 4 4 2;sendevent dev/input/event1 1 528 1;sendevent dev/input/event1 0 0 0;"
            cmd=self.command + " sendevent dev/input/event9 1 311 1;sendevent dev/input/event9 0 0 0;"
            os.system(cmd)
            if self.logger is not None:
                self.logger.log("scanhardKey operation performed",'D')
            return True
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("scanhardKey can't be performed due to:"+str(e),'E')
            return False
        
''' TC70/75 Scan events
/dev/input/event9: 0001 0137 00000001
/dev/input/event9: 0000 0000 00000000
/dev/input/event9: 0001 0137 00000000
/dev/input/event9: 0000 0000 00000000'''


# Class containing functions related to calling related scenarios
class Phone(ModuleFunctions.Phone):

# Ashish- Moved fom Unit class to Phone Class
# ----------------------------------------------------------------------------------------------------------------------
#   makeVoiceCall
#
#   DESCRIPTION
#   Dial a given phone number
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   numberToDial - [Str] Phone number to be dialed
#   Arg. 3.
#   duration - [int] Duration of calls in seconds
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def makeVoiceCall(self, numberToDial, duration=None):

        try:
            print "in riku"
            #Open the phone dialer
            if not self.unit.launchApp(Config.Phone['text']):
                raise Exception("Unable to launch Phone App")
            self.input.wait.update()

            #bring up the dialer pad if we arent already on the dialpad screen
            if not self.unit.exists(uiId=Config.PhoneDial['id']):
                if not self.unit.tapOn(uiId=Config.PhoneDialPad['id']):
                    raise Exception("Couldn't find dialer pad")
            self.input.wait.update()
            time.sleep(1)
            if not self.unit.tapOn(uiId=Config.DialerNumberField['id']):
                    raise Exception("Couldn't find Dialer Number field")
            self.input.wait.update()
            #type the number to dial
            self.unit.typeText(text=numberToDial)
            self.input.wait.update()

            #press the dial icon
            if not self.unit.tapOn(uiId=Config.PhoneDial['id']):
                raise Exception("Couldn't find dialer icon")
            self.input.wait.update()

            #Ashish- added this condition to make this function more flexible
            if duration is not None:
                # wait 'duration' seconds
                time.sleep(duration)
                # hang up the phone
                if not self.unit.tapOn(uiId=Config.PhoneHangup['id']):
                    raise Exception("Couldn't find hang up icon")

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't make voice call due to:"+str(e),'E')
            return False

        
        
#Class containing functions related to Camera related scenarios
class Camera(ModuleFunctions.Camera):
#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   takePicture
#
#   DESCRIPTION
#   launch camera and take picture
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   repetition - number of times picture needs to be taken
#
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def takePicture(self, repetition=1):

        try:
            print "in takePicture"
            #Open the camera
            if not self.unit.launchApp(Config.CameraApp['text']):
                raise Exception("Unable to launch Camera App")
            self.input.wait.update()

            #tap on Camera Switcher
            if not self.unit.tapOn(uiId=Config.CameraSwitcher['id']):
                raise Exception("Unable to tap on Camera Switcher")
            self.input.wait.update()

            #tap on SwitchToPhoto
            if not self.unit.tapOn(uiDescription=Config.SwtchToPhoto['description']):
                raise Exception("Unable to switch to Photo")
            self.input.wait.update()
            time.sleep(1)
            for i in range(repetition):
                #tap on CameraShutter
                if not self.unit.tapOn(uiDescription=Config.CameraShutter['description']):
                    raise Exception("Unable to tap on Shutter")
                self.input.wait.update()
                time.sleep(2)

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("takePicture can't be performed due to:"+str(e),'E')
            return False


#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   takeVideo
#
#   DESCRIPTION
#   launch camera and take video
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   videoDuration - video duration in seconds
#   Arg. 2.
#   repetition - number of times video needs to be taken
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def takeVideo(self, videoDuration=10, repetition=1):

        try:
            print "in takeVideo"
            #Open the camera
            if not self.unit.launchApp(Config.CameraApp['text']):
                raise Exception("Unable to launch Camera App")
            self.input.wait.update()

            #tap on Camera Switcher
            if not self.unit.tapOn(uiId=Config.CameraSwitcher['id']):
                raise Exception("Unable to tap on Camera Switcher")
            self.input.wait.update()

            #tap on SwtchToVideo
            if not self.unit.tapOn(uiDescription=Config.SwtchToVideo['description']):
                raise Exception("Unable to switch to Photo")
            self.input.wait.update()
            time.sleep(1)

            for i in range(repetition):
                #tap on CameraShutter to start video recording
                if not self.unit.tapOn(uiDescription=Config.CameraShutter['description']):
                    raise Exception("Unable to tap on Shutter")
                self.input.wait.update()
                time.sleep(videoDuration)
                #tap on CameraShutter to stop video recording
                if not self.unit.tapOn(uiDescription=Config.CameraShutter['description']):
                    raise Exception("Unable to tap on Shutter")
                self.input.wait.update()
                time.sleep(3)

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("takeVideo can't be performed due to:"+str(e),'E')
            return False



        

# Class containing functions related to WiFi related scenarios
class Wifi(ModuleFunctions.Wifi):

# Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#  connectToWiFi
#
#   DESCRIPTION
#   connect to given WiFi AP
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   APName - Name of the AP to connect
#   Arg. 3.
#   APpassword - password of the AP
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def connectToWiFi(self,APName,APpassword):
        try:
            # Open the Settings App
            if not self.unit.launchApp(Config.SettingApp['text']):
                raise Exception("Unable to launch Settings App")
            self.input.wait.update()

            time.sleep(1)
            # tap on WIfi option
            if not self.unit.tapOn(uiText=Config.WiFi['text'],scrollable=True):
                raise Exception("Unable to tap on Wifi")

            self.input.wait.update()

            # enable WiFi radio if not already on
            if self.unit.exists(Config.WiFiOFF['text']):
                if not self.unit.tapOn(Config.WiFiOFF['text']):
                    raise Exception("Unable to turn on Wifi")
                time.sleep(4)
            self.input.wait.update()

            # tap on given AP Name
            if not self.unit.tapOn(uiText=APName,scrollable=True):
                raise Exception("Unable to tap on given AP ")
            self.input.wait.update()
            time.sleep(1)
            # if it was already connected previously forget it
            if self.unit.exists(uiText=Config.WiFiForget['text']):
                print Config.WiFiForget['text']
                if not self.unit.tapOn(uiText=Config.WiFiForget['text']):
                    raise Exception("unable to click on forget WiFi")
                self.input.wait.update()

                if not self.unit.tapOn(uiText=APName,scrollable=True):
                    raise Exception("Unable to tap on AP Name")
                self.input.wait.update()

            # if not self.unit.tapOn(uiId=Config.WiFiPasswordEditBox['id'],scrollable=True):
                    #raise Exception("Unable to tap on paswword box")
            # self.input.wait.update()
            time.sleep(1)

            # type WiFi password and connect
            self.unit.typeText(APpassword)
            self.input.wait.update()
            if not self.unit.tapOn(uiText=Config.WiFiConnect['text']):
                    raise Exception("Unable to tap on connect ")
            time.sleep(15)

            # verify if able to connect to given wifi
            if not self.unit.exists(uiText=Config.WiFiConnectedText['text'],uiId=Config.WiFiConnectedText['id']):
                raise Exception("Couldn't connect to given AP")

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't connect to WiFi due to:"+str(e),'E')
            return False


# Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   disconnectToWiFi
#
#   DESCRIPTION
#   connect to given WiFi AP
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   APName - Name of the AP to disconnect
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------

    def disconnectToWiFi(self, APName):
        try:
            #Open the Settings App
            if not self.unit.launchApp(Config.SettingApp['text']):
                raise Exception("Unable to launch Settings App")
            self.input.wait.update()

            #tap on WifI option
            if not self.unit.tapOn(uiText=Config.WiFi['text'],scrollable=True):
                raise Exception("Unable to tap on Wifi")

            self.input.wait.update()

            #enable WiFi radio if not already on
            if self.unit.exists(Config.WiFiOFF['text']):
                if not self.unit.tapOn(Config.WiFiOFF['text']):
                    raise Exception("Unable to turn on Wifi")
                time.sleep(4)
            self.input.wait.update()

            # tap given AP name from list
            if not self.unit.tapOn(uiText=APName,scrollable=True):
                raise Exception("Unable to tap on APName")
            self.input.wait.update()
            time.sleep(1)
            #disconnect it by forgeting it
            if self.unit.exists(uiText=Config.WiFiForget['text']):
                if not self.unit.tapOn(uiText=Config.WiFiForget['text']):
                    raise Exception("unable to click on forget WiFi")
                self.input.wait.update()

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't disconnect to WiFi due to:"+str(e),'E')
            return False


#Class containing functions related to WiFi related scenarios
class Browser(ModuleFunctions.Browser):
    pass

#Class containing functions related to Email related scenarios
class Email(ModuleFunctions.Email):
    pass

#Class containing functions related to Scanning related scenarios
class Scanning(ModuleFunctions.Scanning):
    pass