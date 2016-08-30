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
        self.BrowserURLField={'text':'Search or type URL', 'id': 'com.android.chrome:id/url_bar', 'description':None, 'className':'android.widget.EditText'}
        self.Browser={'text':'Chrome', 'id': None, 'description':'Chrome', 'className':'android.widget.TextView'}
        self.GoogleText={'text':'Google', 'id': None, 'description':'Google', 'className':'android.widget.TextView'}
        self.YouAreOfflineText={'text':None, 'id': None, 'description':'You are offline.', 'className':'android.view.View'}
        self.RefreshBtn={'text':None, 'id': 'com.android.chrome:id/refresh_button', 'description':'Refresh page', 'className':'android.widget.ImageButton'}
        self.BookmarkBtn={'text':None, 'id': 'com.android.chrome:id/bookmark_button', 'description':'Bookmark this page', 'className':'android.widget.ImageButton'}
        self.NavigationBtn={'text':None, 'id': 'com.android.chrome:id/navigation_button', 'description':'Site information', 'className':'android.widget.ImageView'}
        self.AppListMultitasking=[('Contacts',True),('Email',True),('Play Music',True),('Photos',True),('Camera',True),('Hangouts',True)]
        self.EmailNavigateUp={'text': None, 'id': None, 'description':'Open navigation drawer', 'className':'android.widget.ImageButton'}
        self.EmailNavigateClose={'text': None, 'id': None, 'description':'Close navigation drawer', 'className':'android.widget.ImageButton'}