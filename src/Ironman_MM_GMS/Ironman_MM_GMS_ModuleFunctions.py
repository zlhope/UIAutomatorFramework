# ----------------------------------------------------------------------------------------------------------------------
# Name Of File: Falcon_MM__ModuleFunctions.py                                                                                #
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
import Ironman_MM_GMS_Config
import ModuleFunctions
Config=Ironman_MM_GMS_Config.Config()

class Unit(ModuleFunctions.Unit):
        
# ----------------------------------------------------------------------------------------------------------------------
#   scanhardKey (TC75)
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


#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   answerCall
#
#   DESCRIPTION
#   Answer call
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   answerCall
#
#   DESCRIPTION
#   Answer call
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def answerCall(self):

        try:
            print "answerCall"
            flag = False
            #wait 30 seconds for incoming call
            for i in range(6):
                #currentActivity=self.unit.getCurrentActivity()
                #check for incoming call
                print self.unit.getCurrentActivity()
                time.sleep(3)
                self.unit.sendKeyEvent('CALL')
                if self.logger is not None:
                    self.logger.log("self.unit.sendKeyEvent('CALL')",'D')
                if self.unit.getCurrentActivity() == Config.IncomingCallActivity['activity']:
                    #send keycode to answer call (http://developer.android.com/reference/android/view/KeyEvent.html#KEYCODE_CALL)
                    flag = True
                    break
                else:
                    print i
                    time.sleep(2)
            return flag

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("answerCall can't be performed due to:"+str(e),'E')
            return flag

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
            if not self.unit.launchApp(Config.SnapdragonCamera['text']):
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
            if not self.unit.launchApp(Config.SnapdragonCamera['text']):
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
            time.sleep(20)

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


#Class containing functions related to Browser related scenarios
class Browser(ModuleFunctions.Browser):

# ----------------------------------------------------------------------------------------------------------------------
#   openWebPage
#
#   DESCRIPTION
#   open given web page from Browser
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   url - Web page link to be opened
#   Arg. 3.
#   Bookmark - Bookmark name to be launched
#   Arg. 4
#   launchBrowser - Flag specifying if Browser needs to be launched or not as part of function
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def openWebPage(self, url=None, Bookmark=None, launchBrowser= True):
        try:

            #Open the Browser App
            if launchBrowser:
                print Config.Browser['text']
                if not self.unit.launchApp(Config.Browser['text']):
                    raise Exception("Unable to launch Browser App")
                self.input.wait.update()

            if url is not None:
                time.sleep(1)
                if self.unit.exists(uiId=Config.BrowserURLField['id']):
                    if not self.unit.tapOn(uiId=Config.BrowserURLField['id']):
                        raise Exception("Unable to tap on BrowserURLField")

                elif self.unit.exists(uiId=Config.BrowserURLBar['id']):
                    if not self.unit.tapOn(uiId=Config.BrowserURLBar['id']):
                        raise Exception("Unable to tap on BrowserURLBar")
                else:
                    raise Exception("Browser URL editbox couldn't be found")

                self.input.wait.update()
                time.sleep(1)
                self.unit.typeText(url)
                self.input.wait.update()
                self.input.press.enter()
                time.sleep(15)

                if self.unit.exists(uiDescription=Config.YouAreOfflineText['description']):

                    raise Exception("Unable to load the webpage, check internet connection")

                self.input.wait.update()

            elif Bookmark is not None:
                self.input.press.menu()
                self.input.wait.update()
                if not self.unit.tapOn(uiText=Config.BookmarksText['text']):
                    if not self.unit.tapOn(uiText=Config.BookmarksText['text'],scrollable=True):
                        raise Exception("Unable to tap on tap on BookmarksText")
                self.input.wait.update()
                time.sleep(1)
                if not self.unit.tapOn(uiText=Bookmark):
                    if not self.unit.tapOn(uiText=Bookmark,scrollable=True):
                        raise Exception("Unable to tap on given Bookmark, please check if the Bookmark is present")
                time.sleep(15)
                if self.unit.exists(uiDescription=Config.YouAreOfflineText['description']):

                    raise Exception("Unable to load the webpage, check internet connection")
                self.input.wait.update()


            else:
                raise Exception("Web url or valid Bookmark name is not provided")

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't open the WebPage due to:"+str(e),'E')
            return False



#Class containing functions related to Email related scenarios
class Email(ModuleFunctions.Email):

# ----------------------------------------------------------------------------------------------------------------------
#   sendEmail
#
#   DESCRIPTION
#   open given web page from Browser
#   Args 6
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   to - email id of receiver
#   Arg. 3.
#   subject - subject line of email
#   Arg. 4
#   body - texts to be entered in Body
#   Arg. 5
#   attachment - name of the attachment
#   Arg. 6
#   launchEmail - Flag specifying if Email needs to be launched or not as part of function
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def sendEmail(self, to, subject=None, body=None, attachment= None,launchEmail=False):
        try:

            #Open the Email App
            if launchEmail:
                print Config.EmailApp['text']
                if not self.unit.launchApp(Config.EmailApp['text']):
                    raise Exception("Unable to launch Email App")
                self.input.wait.update()
            time.sleep(1)
            # check if it is on Inbox Screen
            if self.unit.exists(uiDescription=Config.EmailNavigateUp['description']) and not self.unit.exists(uiText=Config.EmailOutbox['text']):
                self.input.wait.update()
                if not self.unit.tapOn(uiDescription=Config.EmailNavigateUp['description']):
                    raise Exception("Unable to tap on EmailNavigateUp")
                self.input.wait.update()
                time.sleep(1)

                self.input.wait.update()
                time.sleep(1)
                if not self.unit.tapOn(uiText=Config.EmailOutbox['text']):
                    raise Exception("Unable to tap on EmailOutbox")
                self.input.wait.update()
                time.sleep(1)
            else:
                if not self.unit.tapOn(uiText=Config.EmailOutbox['text']):
                    raise Exception("Unable to tap on EmailOutbox")
                self.input.wait.update()
                time.sleep(1)

            if not self.unit.tapOn(uiId=Config.EmailComposeButton['id']):
                raise Exception("Unable to tap on EmailComposeButton")
            self.input.wait.update()
            time.sleep(1)
            self.unit.typeText(to)

            self.unit.sendKeyEvent("TAB")

            if subject is not None:
                if not self.unit.tapOn(uiId=Config.EmailSubjectEditBox['id']):
                    raise Exception("Unable to tap on EmailSubjectEditBox")
                self.input.wait.update()
                time.sleep(1)
                self.unit.typeText(subject)
                self.input.wait.update()
                time.sleep(1)

            if body is not None:
                if not self.unit.tapOn(uiId=Config.EmailBodyEditBox['id']):
                    raise Exception("Unable to tap on EmailBodyEditBox")
                self.input.wait.update()
                time.sleep(1)
                self.unit.typeText(body)
                self.input.wait.update()
                time.sleep(1)

            if attachment is not None:
                if not self.unit.tapOn(uiId=Config.EmailAttachmentButton['id']):
                    raise Exception("Unable to tap on EmailAttachmentButton")
                self.input.wait.update()
                time.sleep(1)
                if not self.unit.tapOn(uiText=Config.EmailAttachFileText['text']):
                    raise Exception("Unable to tap on EmailAttachFileText")
                self.input.wait.update()
                time.sleep(1)
                if self.unit.exists(uiDescription=Config.EmailAttachmentShowRoots['description']):
                    self.input.wait.update()
                    if not self.unit.tapOn(uiDescription=Config.EmailAttachmentShowRoots['description']):
                        raise Exception("Unable to tap on EmailAttachmentShowRoots")
                self.input.wait.update()
                time.sleep(1)
                if not self.unit.tapOn(uiText=Config.EmailAttachRecentText['text']):
                    raise Exception("Unable to tap on EmailAttcahRecentText")
                self.input.wait.update()
                time.sleep(2)
                print attachment
                if not self.unit.exists(uiText=attachment):
                    raise Exception(attachment + "couldn't be found in Recent tab")
                if not self.unit.tapOn(uiText=attachment):
                    raise Exception("Unable to tap on attachment name")
                self.input.wait.update()
                if not self.unit.exists(uiId=Config.EmailSendButton['id']):
                    #print "in if"
                    if not self.unit.tapOn(uiText=attachment):
                        raise Exception("Unable to tap on attachment name")
                        self.input.wait.update()
                        time.sleep(3)
            if not self.unit.tapOn(uiId=Config.EmailSendButton['id']):
                raise Exception("Unable to tap on EmailSendButton")
            self.input.wait.update()
            time.sleep(10)
            if self.unit.exists(uiText=Config.EmailOutboxEmptyMsg['text']):
                self.input.wait.update()

            else:
                time.sleep(10)
                if self.logger is not None:
                    self.logger.log("self.unit.devWidth/2, self.unit.devHeight/2, self.unit.devWidth-5, self.unit.devHeight/2, steps=10",'D')
                self.input.swipe(self.unit.devWidth/2, self.unit.devHeight/7, self.unit.devWidth/2, self.unit.devHeight-50, steps=10)
                self.input.wait.update()
                time.sleep(1)
                if not self.unit.exists(uiText=Config.EmailOutboxEmptyMsg['text']):
                    raise Exception("The Email still in outbox even after 20 seconds")

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't send Email due to:"+str(e),'E')
            return False




#Class containing functions related to Scanning related scenarios
class Scanning(ModuleFunctions.Scanning):
    pass