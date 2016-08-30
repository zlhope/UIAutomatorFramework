# ----------------------------------------------------------------------------------------------------------------------
# Name Of File: ModuleFunctions.py                                                                                #
# Author: Ashish Kumar                                                                                                 #
# Purpose Of File: contains unit level most widely used functions                                                      #
#                                                                                                                      #
# History:                                                                                                             #
# Date                   Author                  Changes                                                               #
# 10/27/2015             Ashish Kumar            First Version                                                         #
# 02/15/2016             Ashish Kumar            Current Version
# ----------------------------------------------------------------------------------------------------------------------
import unittest
import time
import os
import Config
import sys
import subprocess
from pytesser import * #[Ashish]importing python wrapper of tesseract
from PIL import Image, ImageOps #[Ashish]importing required image classes
import re #[Ashish] importing regular expression module
import adb_interface
Config=Config.Config()


class Unit:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId
        self.command="adb -s "+self.device+" wait-for-device shell"
        
        #create an object for AdbInterface
        self.adb = adb_interface.AdbInterface(deviceId)
        manufacturer=self.adb.SendShellCommand("getprop ro.product.manufacturer").strip()
        print manufacturer
        if not (manufacturer == "Zebra Technologies" or manufacturer=="Motorola Solutions"):
            if manufacturer == "error: device not found":
                print "error: device not found"
                if self.logger is not None:
                    self.logger.log("error: device not found",'E')
            else:
                print "Test is running on non Zebra device"
                if self.logger is not None:
                    self.logger.log("Test is running on non Zebra device",'E')
            os._exit(1)
            
        
        #create object variables storing device height & width
        self.devHeight=self.input.info['displayHeight']

        self.devWidth=self.input.info['displayWidth']
        
        #define a handler function for detecting and handling Force close,reboot and ANR
        def fc_close(input):
            try:
                print "in reboot handler"
                if not self.adb.WaitForBootComplete():
                    if self.logger is not None:
                        self.logger.log("Found Reset",'E')
                        self.logger.logReset()
                    return True
                
                print "in FC handler"
                #check if "Unfortunately," text is present in current UI
                obj= self.input(textStartsWith=u"Unfortunately,")
                if obj.exists:
                    print "found FC"
                    #if logger instance is not None, call logger logForceCLose function
                    if self.logger is not None:
                        self.logger.log("Found Force Close",'E')
                        fcText = obj.text
                        self.logger.logForceClose(fcText)
                    #handle force close clickng on "OK" button
                    self.input(text=u'OK').click()
                    return True
                print "in anr handler"
                #check if "Wait" and "OK" texts is present in current UI
                if self.input(textContains=u"Wait").exists and self.input(textContains=u"OK").exists:
                    print "found ANR"
                    #if logger instance is not None, call logger logANR function
                    if self.logger is not None:
                        self.logger.log("Found ANR",'E')
                        self.logger.logANR()
                    #handle force close clickng on "OK" button
                    self.input(text=u'OK').click()
                elif self.input(textContains=u"Camera error"):
                    print "found ANR"
                    #if logger instance is not None, call logger logANR function
                    if self.logger is not None:
                        self.logger.log("Found ANR",'E')
                        self.logger.logANR()
                    #handle force close clickng on "OK" button
                    self.input(text=u'OK').click()
                return True
            except Exception, e:
                print e
        
        #turn on the fc_close handler
        self.input.handlers.on(fc_close)
        

# ----------------------------------------------------------------------------------------------------------------------
#   waitForDevice
#
#   DESCRIPTION
#   Function to check if device is online or not
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#   
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def waitForDevice(self,wait_time=120):
        try:
            
            if not self.adb.WaitForBootComplete(wait_time):
                if self.logger is not None:
                    self.logger.logReset()
                return False
            return True

        except Exception, e:
            print e
            return False
        
    
    
# ----------------------------------------------------------------------------------------------------------------------
#   runShellCommand
#
#   DESCRIPTION
#   Function to check if device is online or not
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#   
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def runAdbCommand(self,cmd,wait_time=120):
        try:
            cmd='wait-for-device '+cmd
            #send command through adb to device 
            if not self.adb.SendCommand(cmd,wait_time):
                if not self.adb.WaitForBootComplete(wait_time):
                    self.logger.logReset()
                return False
            return True

        except Exception, e:
            print e
            return False
    

# ----------------------------------------------------------------------------------------------------------------------
#   launchApp
#
#   DESCRIPTION
#   Function to Launch Application
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   AppName - [Str] Name of application to be launched
#   Arg. 3.
#   verticalScroll- [Boolean] True, if menu icons are to be scrolled vertically
#
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def launchApp(self, AppName, verticalScroll=False):
        
            
        try:
            if verticalScroll:
                #set flag as False
                flag=False
                #Pressing Back and Home just to make sure the screen is at Home screen
                if self.logger is not None:
                    self.logger.log("self.input.press.back()",'D')
                self.input.press.back()
                if self.logger is not None:
                    self.logger.log("self.input.press.back()",'D')
                self.input.press.back()
                if self.logger is not None:
                    self.logger.log("self.input.press.home()",'D')
                self.input.press.home()
                time.sleep(1)
                
                try:
                    if self.logger is not None:
                        self.logger.log("self.input(description="+Config.AppText['description']+").click()",'D')
                    #Click on Apps icon
                     
                    self.input(description=Config.AppText['description']).click()
                except Exception, e:
                    raise Exception("Unable to click on App icon due to :" + str(e))
                    
                
                if self.logger is not None:
                    self.logger.log("self.input.wait.idle()",'D')
                #Wait for device to be idle
                self.input.wait.idle()
                
                
                #if given app exists on screen, click on it
                if self.input(text=AppName).exists:
                    self.input.wait.idle()
                        
                    if self.logger is not None:
                        self.logger.log("self.input(text="+AppName+").click()",'D')
                    self.input(text=AppName).click()
                    self.input.wait.idle()
                    flag = True
            
                return flag
                
                
            else:
                #set flag as False
                flag=False
                #Pressing Back and Home just to make sure the screen is at Home screen
                if self.logger is not None:
                    self.logger.log("self.input.press.back()",'D')
                self.input.press.back()
                if self.logger is not None:
                    self.logger.log("self.input.press.back()",'D')
                self.input.press.back()
                if self.logger is not None:
                    self.logger.log("self.input.press.home()",'D')
                self.input.press.home()
                time.sleep(1)
                try:
                    if self.logger is not None:
                        self.logger.log("self.input(description="+Config.AppText['description']+").click()",'D')
                    #Click on Apps icon
                     
                    self.input(description=Config.AppText['description']).click()
                except Exception, e:
                    raise Exception("Unable to click on App icon due to :" + str(e))
                    
                
                if self.logger is not None:
                    self.logger.log("self.input.wait.idle()",'D')
                #Wait for device to be idle
                self.input.wait.idle()
                
                
                
                # make sure we are on the far left screen
                for x in range(0,5):
                    #print "swiping left"
                    if self.logger is not None:
                        self.logger.log("self.input.swipe(self.devWidth/3, self.devHeight/2, self.devWidth-5, self.devHeight/2, steps=10)",'D')
                    # swipe right to left to first screen
                    if self.logger is not None:
                        self.logger.log("self.devWidth/3, self.devHeight/2, self.devWidth-5, self.devHeight/2, steps=10",'D')
                    self.input.swipe(self.devWidth/3, self.devHeight/2, self.devWidth-5, self.devHeight/2, steps=10)

                #wait for UI to be idle
                if self.logger is not None:
                        self.logger.log("self.input.wait.idle()",'D')
                self.input.wait.idle()
                
                
                
                if self.logger is not None:
                    self.logger.log("loop till UI is on Apps screen",'D')
                #loop till UI is on Apps screen
                for x in range(0, 5):
                    
                    if self.logger is not None:
                        self.logger.log("if given app exists on screen, click on it",'D')
                    #if given app exists on screen, click on it
                    if self.input(text=AppName).exists:
                        self.input.wait.idle()
                        
                        if self.logger is not None:
                            self.logger.log("self.input(text="+AppName+").click()",'D')
                        self.input(text=AppName).click()
                        self.input.wait.idle()
                        flag = True
                        break

                    else:
                        
                        if self.logger is not None:
                            self.logger.log("self.input.swipe(self.devWidth-5, self.devHeight/2, self.devWidth/3, self.devHeight/2, steps=10)",'D')
                        #else swipe left to right to next screen
                        self.input.swipe(self.devWidth-5, self.devHeight/2, self.devWidth/3, self.devHeight/2, steps=10)

                return flag
            
        except Exception, e:
            if self.logger is not None:
                self.logger.log("App couldn't be launched due to *****:"+str(e),'E')
            return flag

# ----------------------------------------------------------------------------------------------------------------------
#   enableDisableCheckbox
#
#   DESCRIPTION
#   Function to select/un-select checkbox
#   Args 6
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   enable - [Bool] Flag to specify whether to enable or disable checkbox
#   Arg. 3.
#   optionText - [Str] The string with the radio box
#   Arg. 4.
#   switchBtn - [Bool] Checkbox type is switch or checkbox, 
#                      for e.g. if checkbox under consideration is WiFi switch 
#                      then its value will be True as here checkbox type is android.widget.Switch
#   Arg. 5.
#   scrollable - [Bool] If the screen is scrollable
#   Arg. 6.
#   checkboxSwitchLocation - ["L" or "R" or None] location of checkbox relative to its text, [this needs to be set None if text and checkbox are same object as seen in uiautomatorviewer]
#   RETURN VALUE
#   Boolean
# --------------------------------------------------------------------------------------------------------------------------------
    def enableDisableCheckbox(self, enable=True, optionText=None, switchBtn=False, scrollable=True, checkboxSwitchLocation="R"):
        try:
            #if optionText is not None
            if optionText is not None:
                #if screen is scrollable
                if scrollable:
                    #scroll screen vertically and find if text is present
                    
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(text="+optionText+")",'D')
                    if self.input(scrollable=True).scroll.to(text=optionText):
                        pass
                    else:
                        raise Exception("Couldn't find the specified checkbox on the screen")
                #if checkbox under consideration is checkbox or switch button
                if switchBtn:
                    checkBoxClassName='android.widget.Switch'
                else:
                    checkBoxClassName='android.widget.CheckBox'
                #if checkbox is located on right or left of text
                if checkboxSwitchLocation == "R":
                    
                    if self.logger is not None:
                        self.logger.log("chckBox = self.input(text="+optionText+").right(className=checkBoxClassName)",'D')
                    chckBox = self.input(text=optionText).right(className=checkBoxClassName)
                elif checkboxSwitchLocation == "L":
                    
                    if self.logger is not None:
                        self.logger.log("chckBox = self.input(text="+optionText+").left(className=checkBoxClassName)",'D')
                    chckBox = self.input(text=optionText).left(className=checkBoxClassName)
                elif checkboxSwitchLocation is None:
                    if self.logger is not None:
                        self.logger.log("chckBox = self.input(text="+optionText+")",'D')
                    chckBox = self.input(text=optionText)
                else:
                    raise Exception("checkboxSwitchLocation not specified")
                #check if checkbox is disabled (greyed out)
                if chckBox.enabled:
                    #if checkbox is already checked
                    if chckBox.checked:
                        #if function called to check or uncheck Checkbox
                        if enable:
                            pass
                        else:
                            #uncheck checkbox
                            
                            if self.logger is not None:
                                self.logger.log("return chckBox.click()",'D')
                            return chckBox.click()
                    else:
                        if enable:
                            #check checkbox
                            
                            if self.logger is not None:
                                self.logger.log("return chckBox.click()",'D')
                            return chckBox.click()
                        else:
                            pass
                else:
                    raise Exception("Checkbox is disabled")
            self.input.wait.idle()
            return True

        except Exception, e:
            if self.logger is not None:
                self.logger.log("enableDisableCheckbox can't be performed due to:"+str(e),'E')
            return False


# ----------------------------------------------------------------------------------------------------------------------
#   checkCheckbox
#
#   DESCRIPTION
#   Function to check status of checkbox
#   Args 5
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   optionText - [Str] The string with the radio box
#   Arg. 3.
#   switchBtn - [Bool] Checkbox type is switch or checkbox
#   Arg. 4.
#   scrollable - [Bool] If the screen is scrollable
#   Arg. 5.
#   checkboxSwitchLocation - ["L" or "R"] location of checkbox relative to its text
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def checkCheckbox(self,optionText=None, switchBtn=False, scrollable=True, checkboxSwitchLocation="R"):
        try:
            #if optionText is not None
            if optionText is not None:
                #if screen is scrollable
                if scrollable:
                    #scroll screen vertically and find if text is present
                    
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(text="+optionText+")",'D')
                    if self.input(scrollable=True).scroll.to(text=optionText):
                        pass
                    else:
                        raise Exception("Couldn't find the specified checkbox on the screen")
                        #if checkbox under consideration is checkbox or switch button
                if switchBtn:
                    checkBoxClassName='android.widget.Switch'
                else:
                    checkBoxClassName='android.widget.CheckBox'
                #if checkbox is located on right or left of text
                if checkboxSwitchLocation == "R":
                    
                    if self.logger is not None:
                        self.logger.log("chckBox = self.input(text="+optionText+").right(className=checkBoxClassName)",'D')
                    chckBox = self.input(text=optionText).right(className=checkBoxClassName)
                elif checkboxSwitchLocation == "L":
                    
                    if self.logger is not None:
                        self.logger.log("chckBox = self.input(text="+optionText+").left(className=checkBoxClassName)",'D')
                    chckBox = self.input(text=optionText).left(className=checkBoxClassName)
                else:
                    raise Exception("checkboxSwitchLocation not specified")
                #return status of checkbox
                return chckBox.checked

        except Exception, e:
            if self.logger is not None:
                self.logger.log("checkCheckbox can't be performed due to:"+str(e),'E')
            return False

# ----------------------------------------------------------------------------------------------------------------------
#   tapOn
#
#   DESCRIPTION
#   Function to tap on given UI element
#   Args 5
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   uiText - [Str] Text value of UI element
#   Arg. 3.
#   uiId - [Str] Resource id of Ui element
#   Arg. 4.
#   uiDescription - [Str] Description value of UI element
#   Arg. 5.
#   scrollable - [Bool] If the screen is scrollable
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def tapOn(self, uiText=None, uiId=None, uiDescription=None, scrollable=False):
        try:
            #check if arguements uiText,uiId and uiDescription is not None
            if uiText is not None and uiId is not None and uiDescription is not None:
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+",description="+uiDescription+")",'D')
                    self.input(scrollable=True).scroll.to(text=uiText, resourceId=uiId,description=uiDescription)
                    #tap on the given UI element
                    
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+", resourceId="+uiId+",description="+uiDescription+").click()",'D')
                    return self.input(text=uiText, resourceId=uiId,description=uiDescription).click()
                else:
                    #tap on the given UI element
                    
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+", resourceId="+uiId+",description="+uiDescription+").click()",'D')
                    return self.input(text=uiText, resourceId=uiId,description=uiDescription).click()
            
            #check if arguements uiText and uiId is not None
            elif uiText is not None and uiId is not None:
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+")",'D')
                    self.input(scrollable=True).scroll.to(text=uiText, resourceId=uiId)
                    #tap on the given UI element
                    
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+").click()",'D')
                    return self.input(text=uiText, resourceId=uiId).click()
                else:
                    #tap on the given UI element
                    
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+").click()",'D')
                    return self.input(text=uiText, resourceId=uiId).click()
            
            #check if arguements uiText and uiDescription is not None
            elif uiText is not None and uiDescription is not None:
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(text="+uiText+",description="+uiDescription+")",'D')
                    self.input(scrollable=True).scroll.to(text=uiText,description=uiDescription)
                    #tap on the given UI element
                    return self.input(text=uiText, description=uiDescription).click()
                else:
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+", description="+uiDescription+").click()",'D')
                    return self.input(text=uiText, description=uiDescription).click()
            
            #check if arguements uiId and uiDescription is not None
            elif uiId is not None and uiDescription is not None:
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(resourceId="+uiId+", description="+uiDescription+")",'D')
                    self.input(scrollable=True).scroll.to(resourceId=uiId, description=uiDescription)
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(resourceId="+uiId+", description="+uiDescription+")",'D')
                    return self.input(resourceId=uiId, description=uiDescription).click()
                else:
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(resourceId="+uiId+", description="+uiDescription+")",'D')
                    return self.input(resourceId=uiId, description=uiDescription).click()
            
            #check if arguements uiText is not None
            elif uiText is not None :
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(text="+uiText+")",'D')
                    self.input(scrollable=True).scroll.to(text=uiText)
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+")",'D')
                    return self.input(text=uiText).click()
                else:
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+").click()",'D')
                    return self.input(text=uiText).click()
            
            #check if arguements uiId is not None
            elif uiId is not None:
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    if self.logger is not None:
                        self.logger.log("self.input(scrollable=True).scroll.to(resourceId="+uiId+")",'D')
                    self.input(scrollable=True).scroll.to( resourceId=uiId)
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(resourceId="+uiId+")",'D')
                    return self.input(resourceId=uiId).click()
                else:
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(resourceId="+uiId+")",'D')
                    return self.input(resourceId=uiId).click()
            
            #check if arguements uiDescription is not None
            elif uiDescription is not None:
                #Check if screen is scrollable 
                if scrollable:
                    #scroll screen vertically and find if arguements are present or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(description="+uiDescription+")",'D')
                    self.input(scrollable=True).scroll.to(description=uiDescription)
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(description="+uiDescription+")",'D')
                    return self.input(description=uiDescription).click()
                else:
                    #tap on the given UI element
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(description="+uiDescription+")",'D')
                    return self.input(description=uiDescription).click()
                
            #raise exceptiom if nothing is specified as arguement
            else:
                raise Exception("No text or id or description specified")

        except Exception, e:
            if self.logger is not None:
                self.logger.log("tapOn can't be performed due to:"+str(e),'E')
            return False

# ----------------------------------------------------------------------------------------------------------------------
#   exists
#
#   DESCRIPTION
#   Function to verify if given UI element exists on screen
#   Args 5
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   uiText - [Str] Text value of UI element
#   Arg. 3.
#   uiId - [Str] Resource id of Ui element
#   Arg. 4.
#   uiDescription - [Str] Description value of UI element
#   Arg. 5.
#   scrollable - [Bool] If the screen is scrollable
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def exists(self, uiText=None, uiId=None, uiDescription=None, scrollable=False):
        try:
            #check if arguements uiText,uiId and uiDescription is not None
            if uiText is not None and uiId is not None and uiDescription is not None:
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+",description="+uiDescription+")",'D')
                    return self.input(scrollable=True).scroll.to(text=uiText, resourceId=uiId,description=uiDescription)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+",description="+uiDescription+").exists",'D')
                    return self.input(text=uiText, resourceId=uiId,description=uiDescription).exists
            
            #check if arguements uiText,uiId is not None
            elif uiText is not None and uiId is not None:
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+", resourceId="+uiId+")",'D')
                    return self.input(scrollable=True).scroll.to(text=uiText, resourceId=uiId)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+", resourceId="+uiId+").exists",'D')
                    return self.input(text=uiText, resourceId=uiId).exists
            
            #check if arguements uiText and uiDescription is not None
            elif uiText is not None and uiDescription is not None:
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+", description="+uiDescription+")",'D')
                    return self.input(scrollable=True).scroll.to(text=uiText,description=uiDescription)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+", description="+uiDescription+").exists",'D')
                    return self.input(text=uiText, description=uiDescription).exists
            
            #check if arguements uiId and uiDescription is not None
            elif uiId is not None and uiDescription is not None:
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(resourceId="+uiId+", description="+uiDescription+")",'D')
                    return self.input(scrollable=True).scroll.to(resourceId=uiId, description=uiDescription)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(resourceId="+uiId+", description="+uiDescription+").exists",'D')
                    return self.input(resourceId=uiId, description=uiDescription).exists
            
            #check if arguements uiText is not None
            elif uiText is not None :
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(text="+uiText+")",'D')
                    return self.input(scrollable=True).scroll.to(text=uiText)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(text="+uiText+").exists",'D')
                    return self.input(text=uiText).exists
                
            #check if arguements uiId is not None
            elif uiId is not None:
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to( resourceId="+uiId+")",'D')
                    return self.input(scrollable=True).scroll.to( resourceId=uiId)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(resourceId="+uiId+").exists",'D')
                    return self.input(resourceId=uiId).exists
            
            #check if arguements uiDescription is not None
            elif uiDescription is not None:
                #Check if screen is scrollable
                if scrollable:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(scrollable=True).scroll.to(description="+uiDescription+")",'D')
                    return self.input(scrollable=True).scroll.to(description=uiDescription)
                else:
                    #return if ui element exists or not
                    if self.logger is not None:
                        self.logger.log("return self.input(description="+uiDescription+")",'D')
                    return self.input(description=uiDescription).exists
                
            #raise exceptiom if nothing is specified as arguement
            else:
                raise Exception("No text or id or description specified")

        except Exception, e:
            if self.logger is not None:
                self.logger.log("exists(self, uiText=None, uiId=None, uiDescription=None, scrollable=False) can't be performed due to:"+str(e),'E')
            return False



# ----------------------------------------------------------------------------------------------------------------------
#   typeText
#
#   DESCRIPTION
#   Function to tap on given UI element
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   text - [Str] Text to be entered
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def typeText(self, text):
        try:
            #check if text not None
            if text is not None:
                counter=0
                #Separate the whole string using " " as delimeter
                word_list=text.split()
                #Get the length of the generated list of words
                length=len(word_list)
                
                while(counter<length):
                    #Input word
                    cmd=' input text "%s"' %word_list[counter]
                    if self.logger is not None:
                        self.logger.log("os.system("+self.command+cmd+")",'D')
                    os.system(self.command+cmd)
                    #If word is not at the end of string then press space 62 is keycode for Space
                    if counter!=(length-1):
                        if self.logger is not None:
                            self.logger.log("os.system("+self.command+cmd+" input keyevent 62)",'D')
                        os.system(self.command+' input keyevent 62')
                    counter=counter+1
                return True
                

        except Exception, e:
            if self.logger is not None:
                self.logger.log("typeText(self, text) can't be performed due to:"+str(e),'E')
            return False


# ----------------------------------------------------------------------------------------------------------------------
#   sendKeyEvent
#
#   DESCRIPTION
#   Function to emulate keyevent using adb
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   keyevent - [Str] Text to be entered
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def sendKeyEvent(self, keyevent):
        try:
            #check if text not None
            if keyevent is not None:
                os.system(self.command+' input keyevent '+keyevent)
                return True

        except Exception, e:
            if self.logger is not None:
                self.logger.log("typeText(self, text) can't be performed due to:"+str(e),'E')
            return False


#[Ashish] added this function
# ----------------------------------------------------------------------------------------------------------------------
#   getCurrentActivity
#
#   DESCRIPTION
#   returns the currently focused activity name
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#
#   RETURN VALUE
#   String[current activity name]
# ----------------------------------------------------------------------------------------------------------------------
    def getCurrentActivity(self):

        try:

            #get dump of current window in pipe
            if self.logger is not None:
                self.logger.log("get dump of current window in pipe",'D')
            self.window_dump=subprocess.Popen(self.command+' dumpsys window windows', shell=False, stdout=subprocess.PIPE)
            #read the pipe as stream of strings
            self.window_dump=self.window_dump.stdout.read()

            # fetch current window
            m=re.search('mCurrentFocus=Window\{(?P<hash>\S*) (?P<title2>\S*) (?P<title>\S*)\S+',self.window_dump)
            #use below regex if string doesn't has "u0"
            #m=re.search('mCurrentFocus=Window\{(?P<hash>\S+) (?P<title>\S*) \S+', self.window_dump)
            if m:
                #group all the matched words
                self.current_window=m.groupdict()
            else:
                self.current_window=None
            print self.current_window['title']

            return self.current_window['title']

        except Exception, e:
            if self.logger is not None:
                self.logger.log("getCurrentActivity can't be performed due to:"+str(e),'E')
            return None

#[Ashish]
# ----------------------------------------------------------------------------------------------------------------------
#   searchTextInImage
#
#   DESCRIPTION
#   Grab the current screen and see if the passed string exists on that screen
#   if it does Move the mouse to the X,Y coords of the string
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   searchText - [str]string to be found on the current screen
#   Arg. 3
#   scrollable - [Bool]if screen is scrollable
#   RETURN VALUE
#   Boolean,all the strings parsed by OCR for the screen
# ----------------------------------------------------------------------------------------------------------------------
    def ocrSearchTextInScreen(self, searchText, scrollable=False):

        try:
            count=0
            FNULL = open(os.devnull, "w")
            # Scroll through screen until the test is found or we run out of screen
            while True:
                
                # Get screenshot
                if self.logger is not None:
                        self.logger.log("capturing screenshot for OCR processing",'D')
                filepath=os.getcwd()+"\\screen.png"
                sceenshotCmd = 'java -jar screenshot.jar -s ' + self.device + ' "' + filepath 
                print sceenshotCmd
                temp = subprocess.call(sceenshotCmd, stdout=FNULL, stderr=subprocess.STDOUT)
                
                #read image as object 
                im = Image.open(os.getcwd()+"\\screen.png")
                #convert the image in buffer to grayscale
                im = im.convert("L")
                
                
                #Ashish- added this enhancement for lesser resolution phones
                #in case screen resolution is small, double the size of image for better OCR operation 
                if im.size[0] < 720:
                    im = im.resize((im.size[0]*2,im.size[1]*2))
                print im.size
                #call pytesser function to convert image content to strings
                text=image_to_string(im)
                print text
                #increase the counter
                count+=1
                #if serach text is found in converted text return true and converted text
                if searchText in text:
                    return True,text
                #if scrollable screen scroll for 5 times and if not find stop
                elif scrollable and count < 5 :
                    self.input(scrollable=True).scroll.vert.forward()
                else:
                    raise Exception("String couldn't be found on the screen")
            
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("ocrSearchTextInScreen(self, searchText, scrollable=False) can't be performed due to:"+str(e),'E')
            return False,None


#Ashish- added this generic function
# ----------------------------------------------------------------------------------------------------------------------
#   getStringOfNextLine
#
#   DESCRIPTION
#   Get the next string from the searched string on the screen
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   searchText - [str]string to be found on the current screen
#   Arg. 3.
#   scrollable - [Bool]if screen is scrollable
#   RETURN VALUE
#   string on next line or None
#  ----------------------------------------------------------------------------------------------------------------------
    def getStringOfNextLine(self, searchText, scrollable=True):

        try:

            #get all the strings from the screen
            texts=self.ocrSearchTextInScreen(searchText,scrollable)
            #if text is found
            if texts[0]:
                #create a list of all the strings shown per line on screen
                textList=texts[1].split('\n')
                #remove empty string items
                while '' in textList:
                    textList.remove('')
                #return the item in next line to  My phone number option in screen
                result=textList[textList.index(searchText)+1]
                print result

                return result
            else:
                raise Exception("The searched string couldn't be found")
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("getStringOfNextLine(self, searchText, scrollable=True) can't be performed due to:"+str(e),'E')
            return None

                
                    
#Ashish- updated function to use "getStringOfNextLine" internally
# ----------------------------------------------------------------------------------------------------------------------
#   getPhoneNumber
#
#   DESCRIPTION
#   Get the phone number of the device
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   searchText - [str]string to be found on the current screen
#   RETURN VALUE
#   phone number or None
#  ----------------------------------------------------------------------------------------------------------------------
    def getPhoneNumber(self, searchText="My phone number"):

        try:
            # get device phone number
            if not self.launchApp(Config.SettingApp['text']):
                raise Exception("Unable to launch Settings App")
            self.input.wait.update()

            # Go to ABOUT PHONE->STATUS
            if not self.tapOn(uiText=Config.AboutText['text'], scrollable=True):
                raise Exception("Couldn't find About Phone selection")
            self.input.wait.update()
            if not self.tapOn(uiText=Config.StatusText['text'], scrollable=True):
                raise Exception("Couldn't find Status selection")
            self.input.wait.update()

            # Some device have the phone number in a submenu called SIM STATUS
            if self.exists(uiText=Config.SIMStatusText['text']):
                self.tapOn(uiText=Config.SIMStatusText['text'])
                self.input.wait.update()
            
            #return the next line to "My phone number" string
            result=self.getStringOfNextLine(searchText,True)
            
            print result

            if result is not None or "Unknown":
                #remove dashes from phone number
                return result.replace('-','')
            else:
                raise Exception("Phone number not found, please check if phone has valid network")
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("getPhoneNumber() can't be performed due to:"+str(e),'E')
            return None
        
        
#Ashish- added this function
# ----------------------------------------------------------------------------------------------------------------------
#   uiElementParser
#
#   DESCRIPTION
#   It parses and returns all the values for searched identifier present on the screen
#   Args 2
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   self - identifier
#   
#   RETURN VALUE
#   list of texts on the screen
#  ----------------------------------------------------------------------------------------------------------------------
    def uiElementParser(self,identifier):

        try:
            screenDump=repr(self.input.dump())
            list=[]
            pattern=identifier+r'="(.*?)"'
            for matches in re.findall(pattern,screenDump):
                if matches is not "":
                    list.append(matches)
            return list
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("uiElementParser can't be performed due to:"+str(e),'E')
            return None
        
                     
#Ashish- added this function
# ----------------------------------------------------------------------------------------------------------------------
#   returnOnScreenTexts
#
#   DESCRIPTION
#   It retuens all the texts present on the screen
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#   
#   RETURN VALUE
#   list of texts on the screen
#  ----------------------------------------------------------------------------------------------------------------------
    def returnOnScreenTexts(self):

        try:
            return self.uiElementParser("text")
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("returnOnScreenTexts can't be performed due to:"+str(e),'E')
            return None
        
        
#Ashish- added this function
# ----------------------------------------------------------------------------------------------------------------------
#   returnOnScreenResourceIds
#
#   DESCRIPTION
#   It retuens all the ResourceIds present on the screen
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#   
#   RETURN VALUE
#   list of texts on the screen
#  ----------------------------------------------------------------------------------------------------------------------
    def returnOnScreenResourceIds(self):

        try:
            return self.uiElementParser("resource-id")
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("returnOnScreenResourceIds can't be performed due to:"+str(e),'E')
            return None


#Ashish- added this function
# ----------------------------------------------------------------------------------------------------------------------
#   returnOnScreenContentDesc
#
#   DESCRIPTION
#   It retuens all the content-desc present on the screen
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#   
#   RETURN VALUE
#   list of texts on the screen
#  ----------------------------------------------------------------------------------------------------------------------
    def returnOnScreenContentDesc(self):

        try:
            return self.uiElementParser("content-desc")
        
        except Exception, e:
            if self.logger is not None:
                self.logger.log("returnOnScreenContentDesc can't be performed due to:"+str(e),'E')
            return None


#Ashish- added this function
# ----------------------------------------------------------------------------------------------------------------------
#   verifyInternetConnection
#
#   DESCRIPTION
#   Checks if device has internet connectivity
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#
#   RETURN VALUE
#   Boolean
#  ----------------------------------------------------------------------------------------------------------------------
    def verifyInternetConnection(self):

        try:
            value=self.adb.SendShellCommand("ping -c1 www.google.com").strip()
            print value
            if "unknown host" in value:
                return False
            return True

        except Exception, e:
            if self.logger is not None:
                self.logger.log("verifyInternetConnection can't be performed due to:"+str(e),'E')
            return None



#Class containing functions related to calling related scenarios
class Phone:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId
        
        #create an object of Unit class
        self.unit=Unit(input, deviceId,logger)
        
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
            print "in makeVoiceCall"
            #Open the phone dialer
            if not self.unit.launchApp(Config.Phone['text']):
                raise Exception("Unable to launch Phone App")
            self.input.wait.update()

            #bring up the dialer pad if we arent already on the dialpad screen
            if self.unit.exists(uiId=Config.PhoneDialPad['id']):
                
                if self.unit.tapOn(uiId=Config.PhoneDialPad['id']):
                    time.sleep(.5)
                    print "tapped dial pad"
                else:
                    raise Exception("Couldn't find dialer pad")
                print " found dialpad"
            self.input.wait.update()
            time.sleep(1)
            #type the number to dial
            if self.unit.exists(uiId=Config.PhoneDial['id']):
                self.unit.typeText(text=numberToDial)
                self.input.wait.update()
            else:
                raise Exception("Couldn't find dialer icon")

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
            if self.logger is not None:
                self.logger.log("makeVoiceCall can't be performed due to:"+str(e),'E')
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
    def answerCall(self):

        try:
            print "answerCall"
            flag = False
            #wait 30 seconds for incoming call
            for i in range(6):
                #currentActivity=self.unit.getCurrentActivity()
                #check for incoming call
                print self.unit.getCurrentActivity()
                if self.unit.getCurrentActivity() == Config.IncomingCallActivity['activity']:
                    #send keycode to answer call (http://developer.android.com/reference/android/view/KeyEvent.html#KEYCODE_CALL)
                    if self.logger is not None:
                        self.logger.log("self.unit.sendKeyEvent('CALL')",'D')
                    self.unit.sendKeyEvent('CALL')
                    flag = True
                    break
                else:
                    print i
                    time.sleep(5)
            return flag

        except Exception, e:
            if self.logger is not None:
                self.logger.log("answerCall can't be performed due to:"+str(e),'E')
            return flag

#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   endCall
#
#   DESCRIPTION
#   End ongoing call
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def endCall(self):

        try:

            if self.unit.getCurrentActivity() == Config.IncomingCallActivity['activity']:
                #send keycode to end call (http://developer.android.com/reference/android/view/KeyEvent.html#KEYCODE_ENDCALL)
                if self.logger is not None:
                        self.logger.log("self.unit.sendKeyEvent('ENDCALL')",'D')
                self.unit.sendKeyEvent('ENDCALL')
            return True

        except Exception, e:
            if self.logger is not None:
                self.logger.log("endCall can't be performed due to:"+str(e),'E')
            return False


#Class containing functions related to Camera related scenarios
class Camera:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId
        
        #create an object of Unit class
        self.unit=Unit(input, deviceId,logger)
        
        
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
                if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
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
                if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                    raise Exception("Unable to tap on Shutter")
                self.input.wait.update()
                time.sleep(videoDuration)
                #tap on CameraShutter to stop video recording
                if not self.unit.tapOn(uiId=Config.CameraShutter['id']):
                    raise Exception("Unable to tap on Shutter")
                self.input.wait.update()
                time.sleep(3)

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("takeVideo can't be performed due to:"+str(e),'E')
            return False
        
        
        
#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   deleteCameraImageVideos
#
#   DESCRIPTION
#   deletes all the video and images from storage(using shell command)
#   Args 1
#   Arg. 1.
#   self - Instance of the self
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------
    def deleteCameraImageVideos(self):

        try:
            flag=True
            if self.unit.runAdbCommand('shell rm -r /mnt/internal/DCIM/*'):
                if self.logger is not None:
                    self.logger.log("Unable to delete camera video and images from internal storage/Or no contents in these locations",'D')
                    
            if self.unit.runAdbCommand('shell rm -r /mnt/sdcard/DCIM/*'):
                if self.logger is not None:
                    self.logger.log("Unable to delete camera video and images from exteranl storage/Or no contents in these locations",'D')
            
            if self.unit.runAdbCommand('shell rm -r /mnt/external/DCIM/*'):
                if self.logger is not None:
                    self.logger.log("Unable to delete camera video and images from exteranl storage/Or no contents in these locations",'D')
                

            return True

        except Exception, e:
            if self.logger is not None:
                self.logger.log("deleteCameraImageVideos can't be performed due to:"+str(e),'E')
            return False



#Class containing functions related to WiFi related scenarios
class Wifi:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId
        
        #create an object of Unit class
        self.unit=Unit(input, deviceId,logger)
 
        
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
            
    def connectToWiFi(self, APName, APpassword):
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
            if self.unit.exists(uiText=Config.WiFiOFF['text']):
                if not self.unit.tapOn(uiText=Config.WiFiOFF['text']):
                    raise Exception("unable to enable WiFi")
                time.sleep(4)
            self.input.wait.update()
            
            #tap on given AP Name
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
            if self.unit.exists(uiText=Config.WiFiOFF['text']):
                if not self.unit.tapOn(uiText=Config.WiFiOFF['text']):
                    raise Exception("unable to enable WiFi")
                time.sleep(4)
            self.input.wait.update()
            
            # tap given AP name from list
            if not self.unit.tapOn(uiText=APName,scrollable=True):
                raise Exception("Unable to tap on tap on given AP")
            self.input.wait.update()
            #disconnect it by forgeting it
            if self.unit.exists(uiText=Config.WiFiForget['text']):
                if not self.unit.tapOn(uiText=Config.WiFiForget['text']):
                    raise Exception("unable to click on forget WiFi")
                
        
            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't disconnect to WiFi due to:"+str(e),'E')
            return False






#Class containing functions related to Browser related scenarios
class Browser:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId
        
        #create an object of Unit class
        self.unit=Unit(input, deviceId,logger)

# ----------------------------------------------------------------------------------------------------------------------
#   openWebPage
#
#   DESCRIPTION
#   open given web page from Browser
#   Args 4
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
                if not self.unit.launchApp(Config.Browser['text']):
                    raise Exception("Unable to launch Browser App")
                self.input.wait.update()
            
            if url is not None:
                time.sleep(1)
                if not self.unit.tapOn(uiId=Config.BrowserURLField['id']):
                    raise Exception("Unable to tap on BrowserURLField")
                self.input.wait.update()
                time.sleep(1)
                self.unit.typeText(url)
                self.input.wait.update()
                self.unit.sendKeyEvent('ENTER')
                time.sleep(10)
                if not self.unit.tapOn(uiId=Config.BrowserFavIcon['id']):
                    raise Exception("Unable to tap on BrowserFavIcon")
                if self.unit.exists(uiText=Config.WebpageNotAvailableText['text']):
                    self.input.press.back()
                    raise Exception("Unable to load the webpage, check url or internet connection")
                    
                self.input.wait.update()
                self.input.press.back()
                
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
                time.sleep(10)
                if not self.unit.tapOn(uiId=Config.BrowserFavIcon['id']):
                    raise Exception("Unable to tap on BrowserFavIcon")
                if self.unit.exists(uiText=Config.WebpageNotAvailableText['text']):
                    self.input.press.back()
                    raise Exception("Unable to load the webpage, check url or internet connection")
                self.input.wait.update()
                self.input.press.back()
                
            else:
                raise Exception("Web url or valid Bookmark name is not provided")

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't open the WebPage due to:"+str(e),'E')
            return False





#Class containing functions related to Email related scenarios
class Email:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId

        #create an object of Unit class
        self.unit=Unit(input, deviceId,logger)

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
class Scanning:
#-----------------------------------------------------------------------------------------------------------------------
#   init
#
#   DESCRIPTION
#   Constructor, called only once, used for creating objects of different classes
#
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   input- Value of input from instance of UIAutomator device
#   Arg. 3.
#   logger- Value of logger from instance of Logger Class
#   RETURN VALUE
#   NA
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, deviceId,logger=None):
        #create object variable for UI Automator instance
        self.input=input
        #create object variable for logger instance
        self.logger=logger
        #create variable to store device id
        self.device=deviceId

        #create an object of Unit class
        self.unit=Unit(input, deviceId,logger)



#Ashish- added this new function
# ----------------------------------------------------------------------------------------------------------------------
#   scanFromDataWedge
#
#   DESCRIPTION
#   scan barcode from DataWedge App
#   Args 3
#   Arg. 1.
#   self - Instance of the self
#   Arg. 2.
#   barcodeValue - value of barcode to be read
#   Arg. 2.
#   launchDatawedge - True
#   RETURN VALUE
#   Boolean
# ----------------------------------------------------------------------------------------------------------------------

    def scanFromDataWedge(self,launchDatawedge=False):
        try:
            #Open the DWDemo App
            if launchDatawedge:
                if not self.unit.launchApp(Config.DWDemoApp['text']):
                    raise Exception("Unable to launch DWDemo App")
                self.input.wait.update()
            time.sleep(1)
            oldLen=0
            #check if barcode is already available
            if not len(self.unit.returnOnScreenTexts()) <= 1:
                oldLen=len(self.unit.returnOnScreenTexts()[1].split('&#10;'))
                print oldLen

            if not self.unit.tapOn(uiId=Config.DWSoftScanBtn['id']):
                raise Exception("Unable to tap on DWSoftScanBtn")
            self.input.wait.update()
            time.sleep(2)
            newLen=len(self.unit.returnOnScreenTexts()[1].split('&#10;'))
            print newLen

            if not (oldLen+1)==newLen:
                raise Exception("new barcode scan resulted null")

            return True

        except Exception, e:
            print e
            if self.logger is not None:
                self.logger.log("couldn't scan From DataWedge due to:"+str(e),'E')
            return False

