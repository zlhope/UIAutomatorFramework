import os
import sys
rootDir= '\\'.join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, rootDir)
import Config
baseClass=Config.Config
#Config file for Falcon
# it should contain only the constants thats is used by falxon_MM_ModuleFunctions exclusively
# format is same as main config file, e.g.BluetoothOption={'text':'Bluetooth', 'id': None, 'description':None, 'className':'android.widget.TextView'}
#phone Constants
class Config(baseClass):
    
    def __init__(self):
        
        baseClass.__init__(self)
        self.SwtchToPhoto={'text':u'Camera', 'id':'com.android.camera2:id/selector_text', 'description':None, 'className':'android.widget.TextView'}
        self.SwtchToVideo={'text':u'Video', 'id':'com.android.camera2:id/selector_text', 'description':None, 'className':'android.widget.TextView'}

        self.MoreOptions={'text':None, 'id':None, 'description':'More options', 'className':'android.widget.ImageButton'}
        self.PageInfo={'text':'Page info', 'id':'android:id/title', 'description':None, 'className':'android.widget.TextView'}

        self.EmailNavigateUp={'text': None, 'id': None, 'description':'Open navigation drawer', 'className':'android.widget.ImageButton'}
        self.EmailNavigateClose={'text': None, 'id': None, 'description':'Close navigation drawer', 'className':'android.widget.ImageButton'}
        self.AppListMultitasking=[('Contacts',False),('Email',False),('Music',False),('Gallery',False),('Camera',False)]