# ----------------------------------------------------------------------------------------------------------------------
# Name Of File: MC40_LL_ModuleFunctions.py                                                                                #
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
import WT6000_LL_Config
import ModuleFunctions
Config=WT6000_LL_Config.Config()

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


#Class containing functions related to calling related scenarios
class Phone(ModuleFunctions.Phone):
    pass
        
        
#Class containing functions related to Camera related scenarios
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
            
            time.sleep(1)
            #tap on WIfi option
            if not self.unit.tapOn(uiText=Config.WiFi['text'],scrollable=True):
                raise Exception("Unable to tap on Wifi")

            self.input.wait.update()
            
            #enable WiFi radio if not already on
            if self.unit.exists(Config.WiFiOFF['text']):
                if not self.unit.tapOn(Config.WiFiOFF['text']):
                    raise Exception("Unable to turn on Wifi")
                time.sleep(4)
            self.input.wait.update()
            
            #tap on given AP Name
            if not self.unit.tapOn(uiText=APName,scrollable=True):
                raise Exception("Unable to tap on given AP ")
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
    pass

#Class containing functions related to Email related scenarios
class Email(ModuleFunctions.Email):
    pass

#Class containing functions related to Scanning related scenarios
class Scanning(ModuleFunctions.Scanning):
    pass