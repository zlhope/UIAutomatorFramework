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
import TC75_KK_Config
import ModuleFunctions
Config=TC75_KK_Config.Config()


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
    pass

#Class containing functions related to Browser related scenarios
class Browser(ModuleFunctions.Browser):
    pass
#Class containing functions related to Email related scenarios
class Email(ModuleFunctions.Email):
    pass

#Class containing functions related to Scanning related scenarios
class Scanning(ModuleFunctions.Scanning):
    pass