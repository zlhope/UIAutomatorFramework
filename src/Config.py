#Common Constants
class Config:
    def __init__(self):
        

        self.AppIcon={'text':None, 'id': None, 'description':'Apps', 'className':'android.widget.TextView'}
        self.WidgetText={'text':None, 'id': None, 'description':'Widgets', 'className':'android.widget.TextView'}
        self.AppText={'text':'Apps', 'id': None, 'description':'Apps', 'className':'android.widget.TextView'}
        self.Browser={'text':'Browser', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        #self.BrowserURLField={'text':'Search or type URL', 'id': 'com.android.browser:id/url', 'description':None, 'className':'android.widget.EditText'}
        self.Messaging={'text':'Messaging', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.MessagingActionComposeNew={'text':None, 'id': 'com.android.mms:id/action_compose_new', 'description':'New message', 'className':'android.widget.TextView'}
        self.MessagingTO={'text':'Type name or number', 'id': 'com.android.mms:id/recipients_editor', 'description':None, 'className':'android.widget.MultiAutoCompleteTextView'}
        self.MessagingMSG={'text':'Type message', 'id': 'com.android.mms:id/embedded_text_editor', 'description':None, 'className':'android.widget.EditText'}
        self.MessagingSEND={'text':None, 'id': 'com.android.mms:id/send_button_sms', 'description':'Send', 'className':'android.widget.ImageButton'}
        self.MessagingDeleteAllThreads={'text':'Delete all threads', 'id': 'android:id/title', 'description':None, 'className':'android.widget.ImageButton'}
        self.MessagingDeleteAllThreadsConfirmation={'text':'Delete', 'id': 'android:id/button1', 'description':None, 'className':'android.widget.Button'}
        self.MessagingMoreOptions={'text':None, 'id': None, 'description':'More options', 'className':'android.widget.ImageButton'}

        #DataWedge
        self.DataWedge={'text':'DataWedge', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.DataWedgeProfile0={'text':'Profile0 (default)', 'id': 'android:id/text1', 'description':None, 'className':'android.widget.TextView'}
        self.DataWedgeProfileEnable={'text':'Profile enabled', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}

        #Settings Constants
        self.SettingApp={'text':'Settings', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.BluetoothOption={'text':'Bluetooth', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.DisplayOptiont={'text':'Display', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.AutoRotateScreenText={'text':'Auto-rotate screen', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.Sleep={'text':'Sleep', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.Sleep15Seconds={'text':'15 seconds', 'id': 'android:id/text1', 'description':None, 'className':'android.widget.CheckedTextView'}
        self.AboutText={'text':'About phone', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.StatusText={'text':'Status', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.SIMStatusText={'text':'SIM status', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}

        #Wi-Fi
        self.WiFi={'text':(u'Wi\u2011Fi'), 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.WiFiOFF={'text':'OFF', 'id': None, 'description':None, 'className':'android.widget.Switch'}
        self.WiFiON={'text':'ON', 'id': None, 'description':None, 'className':'android.widget.Switch'}
        self.WiFiForget={'text':'Forget', 'id': 'android:id/button3', 'description':None, 'className':'android.widget.Button'}
        self.WiFiConnect={'text':'Connect', 'id': 'android:id/button1', 'description':None, 'className':'android.widget.Button'}
        self.WiFiPasswordEditBox={'text':None, 'id': 'com.android.settings:id/password', 'description':None, 'className':'android.widget.EditText'}
        self.WiFiConnectedText={'text':'Connected', 'id': 'android:id/summary', 'description':None, 'className':'android.widget.TextView'}
        
        #Bluetooth
        self.BT={'text':('Bluetooth'), 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.BTOFF={'text':'OFF', 'id': None, 'description':None, 'className':'android.widget.Switch'}
        self.BTON={'text':'ON', 'id': None, 'description':None, 'className':'android.widget.Switch'}
        self.BTRenameMenu={'text':'Rename phone', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.BTRenameButton={'text':'Rename', 'id': 'android:id/button1', 'description':None, 'className':'android.widget.Button'}
        self.BTOnlyVisible={'text':'Only visible to paired devices', 'id': 'android:id/summary', 'description':None, 'className':'android.widget.TextView'}
        self.BTSearchForDevices={'text':'Search for devices', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.BTPair={'text':'Pair', 'id': 'android:id/button1', 'description':None, 'className':'android.widget.Button'}

        #BTSERVER.APK
        self.BTServerAppConfigure={'text':'Configure', 'id': 'com.symbol.etg.bluetoothserver:id/configureServerButton', 'description':None, 'className':'android.widget.Button'}
        self.BTServerAppStart={'text':'Start', 'id': 'com.symbol.etg.bluetoothserver:id/startServerButton', 'description':None, 'className':'android.widget.Button'}
        self.BTServerApp={'text':'Bluetooth Server', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.BTServerAppConfigureConnection={'text':'Secure Connection', 'id': 'com.symbol.etg.bluetoothserver:id/secureCheckBox', 'description':None, 'className':'android.widget.CheckBox'}
        self.BTServerAppSave={'text':'Save', 'id': 'com.symbol.etg.bluetoothserver:id/saveConfigurationButton', 'description':None, 'className':'android.widget.Button'}

        #Phone RESET
        self.Reset={'text':'Backup & reset', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.EnterpriseReset={'text':'Enterprise data reset', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.ResetPhone={'text':'Reset phone', 'id': 'com.android.settings:id/initiate_master_clear', 'description':None, 'className':'android.widget.Button'}
        self.EraseEverything={'text':'Erase everything', 'id': 'com.android.settings:id/execute_master_clear', 'description':None, 'className':'android.widget.Button'}

        #phone Constants
        self.Phone={'text':'Phone', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.PhoneDialPad={'text':None, 'id': 'com.android.dialer:id/dialpad_button', 'description':'dial pad', 'className':'android.widget.TextView'}
        self.PhoneDial={'text':None, 'id': 'com.android.dialer:id/dial_button', 'description':'dial', 'className':'android.widget.ImageButton'}

        self.PhoneHangup={'text':None, 'id': 'com.android.dialer:id/endButton', 'description':'End', 'className':'android.widget.ImageButton'}
        self.IncomingCallActivity={'text':None,'description':None, 'className':None, 'activity':'com.android.dialer/com.android.incallui.InCallActivity'}

        #Camera Constants
        self.CameraApp={'text':u'Camera', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.CameraShutter={'text':None, 'id': 'com.android.camera2:id/shutter_button', 'description':'Shutter', 'className':'android.widget.ImageView'}
        self.CameraSwitcher={'text':None, 'id': 'com.android.camera2:id/camera_switcher', 'description':None, 'className':'android.widget.ImageView'}
        self.SwtchToVideo={'text':None, 'id': None, 'description':u'Switch to video', 'className':'android.widget.ImageView'}
        self.SwtchToPhoto={'text':None, 'id': None, 'description':u'Switch to photo', 'className':'android.widget.ImageView'}
        self.SwtchToPanorama={'text':None, 'id': None, 'description':u'Switch to panorama', 'className':'android.widget.ImageView'}
        
        
        
        #Browser Constants
        self.BrowserURLField={'text':u'Sabout:blank', 'id': 'com.android.browser:id/url', 'description':None, 'className':'android.widget.EditText'}
        self.BrowserTabSwitcher={'text':None, 'id': 'com.android.browser:id/tab_switcher', 'description':'Page manager', 'className':'android.widget.ImageButton'} 
        self.BrowserFavIcon={'text':None, 'id': 'com.android.browser:id/favicon', 'description':None, 'className':'android.widget.ImageView'} 
        self.WebpageNotAvailableText={'text':u'Webpage not available', 'id': 'com.android.browser:id/title', 'description':None, 'className':'android.widget.TextView'} 
        self.RefreshText={'text':u'Refresh', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.SettingsText={'text':u'Settings', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.BookmarksText={'text':u'Bookmarks', 'id': 'android:id/title', 'description':None, 'className':'android.widget.TextView'}
        
        
        #Contact Constants
        self.PeopleApp={'text':u'People', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        
        #Gallery Constants
        self.GalleryApp={'text':u'Gallery', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        
        #Music Constants
        self.MusicApp={'text':u'Music', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        
        #Email Constants
        self.EmailApp={'text':u'Email', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.EmailWelcomeActivity="com.android.email/com.android.email.activity.Welcome"
        self.EmailComposeButton={'text':None, 'id': 'com.android.email:id/compose_button', 'description':None, 'className':'android.widget.ImageButton'}
        self.EmailToEditBox={'text':None, 'id': 'com.android.email:id/to', 'description':None, 'className':'android.widget.MultiAutoCompleteTextView'}
        self.EmailSubjectEditBox={'text':'Subject', 'id': 'com.android.email:id/subject', 'description':None, 'className':'android.widget.EditText'}
        self.EmailBodyEditBox={'text':'Compose email', 'id': 'com.android.email:id/body', 'description':None, 'className':'android.widget.EditText'}
        self.EmailSendButton={'text':None, 'id': 'com.android.email:id/send', 'description':'Send', 'className':'android.widget.TextView'}
        self.EmailAttachmentButton={'text':None, 'id': 'com.android.email:id/add_attachment', 'description':'Attach file', 'className':'android.widget.TextView'}
        self.EmailAttachFileText={'text':'Attach file', 'id': 'com.android.email:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.EmailAttachVideosText={'text':'Videos', 'id': 'com.android.email:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.EmailAttachAudioText={'text':'Audio', 'id': 'com.android.email:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.EmailAttachImagesText={'text':'Images', 'id': 'com.android.email:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.EmailAttachRecentText={'text':'Recent', 'id': 'com.android.email:id/title', 'description':None, 'className':'android.widget.TextView'}
        self.EmailNavigateUp={'text': None, 'id': None, 'description':'Navigate up', 'className':'android.widget.ImageButton'}
        self.EmailInbox={'text': 'Inbox', 'id': 'com.android.email:id/name', 'description':None, 'className':'android.widget.TextView'}
        self.EmailAttachmentShowRoots={'text': None, 'id': None, 'description':'Show roots', 'className':'android.widget.ImageButton'}
        self.EmailOutbox={'text': 'Outbox', 'id': 'com.android.email:id/name', 'description':None, 'className':'android.widget.TextView'}
        self.EmailOutboxEmptyMsg={'text': 'There is no mail here.', 'id': 'com.android.email:id/empty_text', 'description':None, 'className':'android.widget.TextView'}
        self.EmailSubjectLine="Test mails"
        self.EmailBodyLine="This is test Email.Please Ignore!"


        #AppList
        self.AppListMultitasking=[('People',False),('Email',False),('Phone',False),('Music',False),('Gallery',False),('Camera',False),('Messaging',False)]
        self.TopWebsites=['www.att.com','www.yahoo.com', 'www.facebook.com', 'www.youtube.com' ,'www.nytimes.com']



        #DataWedge Constants
        self.DWDemoApp={'text':u'DWDemo', 'id': None, 'description':None, 'className':'android.widget.TextView'}
        self.DWSoftScanBtn={'text':None, 'id': 'com.symbol.datawedge:id/softscanbutton', 'description':'DataWedge Demo', 'className':'android.widget.ImageButton'}
        self.DWOutputView={'text':None, 'id': 'com.symbol.datawedge:id/output_view', 'description':None, 'className':'android.widget.TextView'}


