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
        self.AppListMultitasking=[('Contacts', False), ('Email', False), ('Music', False), ('Gallery', False),
                                  ('Camera', False), ('Phone', False), ('Messaging', False)]
        self.PhoneDialPad={'text':None, 'id': 'com.android.dialer:id/floating_action_button', 'description':'dial pad', 'className':'android.widget.ImageButton'}
        self.PhoneDial={'text':None, 'id': 'com.android.dialer:id/dialpad_floating_action_button', 'description':'dial', 'className':'android.widget.ImageButton'}
        self.DialerNumberField={'text':None, 'id': 'com.android.dialer:id/digits', 'description': None, 'className':'android.widget.EditText'}
        self.SnapdragonCamera={'text':'Snapdragon Camera', 'id': None, 'description': None, 'className':'android.widget.TextView'}
        self.CameraSwitcher= {'text':None, 'id': 'org.codeaurora.snapcam:id/camera_switcher', 'description': u'Camera, video, or panorama selector', 'className':'android.widget.ImageView'}
        self.CameraShutter= {'text':None, 'id': 'org.codeaurora.snapcam:id/shutter_button', 'description': u'Shutter', 'className':'org.codeaurora.snapcam'}
        self.WlanText= {'text':'WLAN', 'id': None, 'description': None, 'className':'android.widget.TextView'}
        self.WiFi={'text':u'Wi\u2011Fi', 'id': None, 'description': None, 'className':'android.widget.TextView'}

        self.Browser={'text':'Chrome', 'id': None, 'description':'Chrome', 'className':'android.widget.TextView'}
        self.BrowserURLField={'text':u'Search or type URL', 'id': 'com.android.chrome:id/search_box_text', 'description':None, 'className':'android.widget.EditText'}
        self.BrowserURLBar={'text':u'Search or type URL', 'id': 'com.android.chrome:id/url_bar', 'description':None, 'className':'android.widget.EditText'}
        self.GoogleText={'text':'Google', 'id': None, 'description':'Google', 'className':'android.widget.TextView'}
        self.YouAreOfflineText={'text':None, 'id': None, 'description':'You are offline.', 'className':'android.view.View'}
        #self.RefreshBtn={'text':None, 'id': 'com.android.chrome:id/refresh_button', 'description':'Refresh page', 'className':'android.widget.ImageButton'}
        #self.BookmarkBtn={'text':None, 'id': 'com.android.chrome:id/bookmark_button', 'description':'Bookmark this page', 'className':'android.widget.ImageButton'}
        #self.NavigationBtn={'text':None, 'id': 'com.android.chrome:id/navigation_button', 'description':'Site information', 'className':'android.widget.ImageView'}
        #AppList
        self.AppListMultitasking=[('Contacts',False),('Gmail',False),('DWDemo',False),('DataWedge',False),('Gallery',False),('Maps',False),('Messenger',False), ('Clock',False),
                                  ('Settings',False),('Snapdragon Camera',False),('Play Music',False)]


        #Email Constants
        self.EmailApp={'text':u'Gmail', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.EmailWelcomeActivity="com.google.android.gm/.ConversationListActivityGmail"
        self.EmailComposeButton={'text':None, 'id': 'com.google.android.gm:id/compose_button', 'description':None, 'className':'android.widget.ImageButton'}
        self.EmailToEditBox={'text':None, 'id': 'com.google.android.gm:id/to', 'description':None, 'className':'android.widget.MultiAutoCompleteTextView'}
        self.EmailSubjectEditBox={'text':'Subject', 'id': 'com.google.android.gm:id/subject', 'description':None, 'className':'android.widget.EditText'}
        self.EmailBodyEditBox={'text':'Compose email', 'id': 'com.google.android.gm:id/body', 'description':None, 'className':'android.widget.EditText'}
        self.EmailSendButton={'text':None, 'id': 'com.google.android.gm:id/send', 'description':'Send', 'className':'android.widget.TextView'}
        self.EmailAttachmentButton={'text':None, 'id': 'com.google.android.gm:id/add_attachment', 'description':'Attach file', 'className':'android.widget.TextView'}

        self.EmailInbox={'text': 'Primary', 'id': 'com.google.android.gm:id/name', 'description':None, 'className':'android.widget.TextView'}

        self.EmailOutbox={'text': 'Outbox', 'id': 'com.android.email:id/name', 'description':None, 'className':'android.widget.TextView'}
        self.EmailOutboxEmptyMsg={'text': 'There is no mail here.', 'id': 'com.google.android.gm:id/empty_text', 'description':None, 'className':'android.widget.TextView'}
        self.EmailSubjectLine="Test mails"
        self.EmailBodyLine="This is test Email.Please Ignore!"
