#Config file for MC40
# it should contain only the constants thats is used by MC40_KK_ModuleFunctions exclusively
# format is same as main config file, e.g.BluetoothOption={'text':'Bluetooth', 'id': None, 'description':None, 'className':'android.widget.TextView'}
import os
import sys
rootDir= '\\'.join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, rootDir)
import Config
baseClass=Config.Config

class Config(baseClass):
    
    def __init__(self):
        
        baseClass.__init__(self)
        