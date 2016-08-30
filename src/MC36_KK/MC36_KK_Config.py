import os
import sys
rootDir= '\\'.join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, rootDir)
import Config
baseClass=Config.Config
#Config file for MC36
# it should contain only the constants thats is used by MC36_KK_ModuleFunctions exclusively
# format is same as main config file, e.g.BluetoothOption={'text':'Bluetooth', 'id': None, 'description':None, 'className':'android.widget.TextView'}

class Config(baseClass):
    
    def __init__(self):
        
        baseClass.__init__(self)
        self.PhoneDial={'text':None, 'id': 'com.android.dialer:id/dialButton', 'description':'dial', 'className':'android.widget.ImageButton'}
        self.WifiSwitchButton={'text':None, 'id': 'com.mediatek:id/imageswitch', 'description':None, 'className':'android.widget.Switch'}