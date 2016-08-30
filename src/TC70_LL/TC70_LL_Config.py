import os
import sys
rootDir= '\\'.join(os.getcwd().split('\\')[:-1])
sys.path.insert(0, rootDir)
import Config
baseClass=Config.Config
#Config file for TC75
# it should contain only the constants thats is used by TC70_KK_ModuleFunctions exclusively
# format is same as main config file, e.g.BluetoothOption={'text':'Bluetooth', 'id': None, 'description':None, 'className':'android.widget.TextView'}
#phone Constants
class Config(baseClass):
    
    def __init__(self):
        
        baseClass.__init__(self)
        self.AppListMultitasking=[('Contacts', False), ('Email', False), ('Music', False), ('Gallery', False),
                                  ('Camera', False), ('Phone', False), ('Messaging', False)]
        self.PhoneDialPad={'text':None, 'id': 'com.android.dialer:id/floating_action_button', 'description':'dial pad', 'className':'android.widget.ImageButton'}
        self.PhoneDial={'text':None, 'id': 'com.android.dialer:id/dialpad_floating_action_button', 'description':'dial', 'className':'android.widget.ImageButton'}
        self.DialerNumberField={'text':None, 'id': 'com.android.dialer:id/digits', 'description': None, 'className':'android.widget.EditText'}
        self.CameraSwitcher= {'text':None, 'id': 'org.codeaurora.snapcam:id/camera_switcher', 'description': u'Camera, video, or panorama selector', 'className':'android.widget.ImageView'}
        self.CameraShutter= {'text':None, 'id': 'org.codeaurora.snapcam:id/shutter_button', 'description': u'Shutter', 'className':'android.widget.ImageView'}