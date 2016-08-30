# ----------------------------------------------------------------------------------------------------------------------
# Name Of File: MC36_KK_ModuleFunctions.py                                                                                #
# Author: Ashish Kumar                                                                                                 #
# Purpose Of File: contains unit level most widely used functions                                                      #
#                                                                                                                      #
# History:                                                                                                             #
# Date                   Author                  Changes                                                               #
# 12/08/2016             Ashish Kumar            First Version                                                         #
#                                                       #
#----------------------------------------------------------------------------------------------------------------------
import os
import sys
rootDir= '\\'.join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, rootDir)
import time
import MC36_KK_Config
import ModuleFunctions
#import os.path
#print os.path.abspath(ModuleFunctions.__file__)
Config=MC36_KK_Config.Config()


class Unit(ModuleFunctions.Unit):
        
# ----------------------------------------------------------------------------------------------------------------------
#   scanhardKey (MC36)
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
            cmd=self.command+" sendevent dev/input/event0 1 311 1;sendevent dev/input/event0 0 0 0;"
            
            os.system(cmd)
            time.sleep(2)
            #key up kernel event for scan button
            cmd=self.command+" sendevent dev/input/event0 1 311 0;sendevent dev/input/event0 0 0 0;"
            
            os.system(cmd)
        
        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't scan due to:"+str(e),'E')
            return False
            return False
        



#Class containing functions related to calling related scenarios
class Phone(ModuleFunctions.Phone):
    #Ashish- Moved fom Unit class to Phone Class
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
        
        
class Camera(ModuleFunctions.Camera):
    pass

#Class containing functions related to WiFi related scenarios
class Wifi(ModuleFunctions.Wifi):

#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   connectToWiFi
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
            #Open the Settings App
            if not self.unit.launchApp(Config.SettingApp['text']):
                raise Exception("Unable to launch Settings App")
            self.input.wait.update()

            #tap on WiFi Text
            if not self.unit.tapOn(uiText=Config.WiFi['text'],scrollable=True):
                raise Exception("Unable to tap on WiFi option")
            self.input.wait.update()
            
            #enable WifI radio if already not enabled
            if not self.input(resourceId=Config.WifiSwitchButton['id']).checked:
                if not self.unit.tapOn(uiId=Config.WifiSwitchButton['id']):
                    raise Exception("unable to enable WiFi")
                time.sleep(4)
            self.input.wait.update()
            
            # tap on given AP from list 
            if not self.unit.tapOn(uiText=APName,scrollable=True):
                raise Exception("Unable to tap on given AP")
            self.input.wait.update()
            
            #if it was already connected previously forget it
            if self.unit.exists(uiText=Config.WiFiForget['text']):
                if not self.unit.tapOn(uiText=Config.WiFiForget['text']):
                    raise Exception("unable to click on forget WiFi")
                self.input.wait.update()
                    
                if not self.unit.tapOn(uiText=APName,scrollable=True):
                    raise Exception("Unable to tap on AP Name")
                self.input.wait.update()
            
            #if not self.unit.tapOn(uiId=Config.WiFiPasswordEditBox['id'],scrollable=True):
                    #raise Exception("Unable to tap on paswword box")
            #self.input.wait.update()
            time.sleep(1)
            # type WiFi password and connect
            self.unit.typeText(APpassword)
            self.input.wait.update()
            if not self.unit.tapOn(uiText=Config.WiFiConnect['text']):
                    raise Exception("Unable to tap on connect ")
            time.sleep(15)
            # verify if able to connect to given wifi
            if not self.unit.exists(uiText=Config.WiFiConnectedText['text'],uiId=Config.WiFiConnectedText['id'],scrollable=True):
                raise Exception("Couldn't connect to given AP")
        
            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't connect to WiFi due to:"+str(e),'E')
            return False


       
#Ashish- added this new function
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

            #tap on WiFi Text
            if not self.unit.tapOn(uiText=Config.WiFi['text'],scrollable=True):
                raise Exception("Unable to tap on WiFi option")
            self.input.wait.update()
            
            #enable WiFi radio if not already on
            if not self.input(resourceId=Config.WifiSwitchButton['id']).checked:
                if not self.unit.tapOn(uiId=Config.WifiSwitchButton['id']):
                    raise Exception("unable to enable WiFi")
                time.sleep(4)
            self.input.wait.update()
            
            # tap given AP name from list
            if not self.unit.tapOn(uiText=APName,scrollable=True):
                raise Exception("Unable to tap on given AP")
            self.input.wait.update()
            
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