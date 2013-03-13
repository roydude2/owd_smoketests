#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from tools      import TestUtils
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_settings import *
from apps.app_browser import *

class test_31(GaiaTestCase):
    _Description = "Use Data Connection to download packaged app."
    
    _URL         = "http://everlong.org/mozilla/packaged/"
    _appName     = "cool packaged app"
    _appOK       = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 31)
        self.Settings   = AppSettings(self)
        self.Browser    = AppBrowser(self)
        
        #
        # Ensure we have a connection.
        #
        self.data_layer.disable_wifi()
        self.Settings.trun_dataConn_on_if_required()
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Uninstall the app (if need be).
        #
        try: self.apps.uninstall(self._appName)
        except: pass #(ignore any exceptions)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Wifi needs to be off for this test to work.
        #
        self.Settings.turn_dataConn_on(True)
        
        #
        # Open the browser app.
        #
        self.Browser.launch()
        
        #
        # Open our URL.
        #
        self.Browser.open_url(self._URL)

        #
        # Check the page didn't have a problem.
        #
        self.Browser.check_page_loaded()
        
        #
        # Install the app (these DOM items are peculiar to this little dev app,
        # so dont bother putting them in the main DOM.py file).
        #
        x = ('id', 'install-app')        
        install_btn = self.UTILS.get_element(*x)
        self.marionette.tap(install_btn)
        
        # Install button on the splash screen (switch to main frame to 'see' this).
        self.marionette.switch_to_frame()

        x = ('id', 'app-install-install-button')        
        install_btn = self.UTILS.get_element(*x)
        self.marionette.tap(install_btn)
        
        # ... and switch back to brwoser to see the next splash screen(!)
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        x = ('id', 'modal-dialog-alert-ok')
        btn = self.UTILS.get_element(*x)
        self.marionette.tap(btn)

        #
        # Go back to the home page and check the app is installed.
        #
        self.UTILS.TEST(self.UTILS.isAppInstalled(self._appName), "App icon not found in homescreen.")
        
        self._appOk = True
        try: 
            self.apps.launch(self._appName)
        except:
            self._appOk = False
        
        self.UTILS.TEST(self._appOk, "App failed to launch.", True)

        #
        # Make sure the app launched (just check 'anything' from the app is 'there').
        #
        self._appOk = True
        try: 
            x = ('xpath', '//title[text()="Template"]')
            self.wait_for_element_present(*x)
        except:
            self._appOk = False
        
        self.UTILS.TEST(self._appOk, "App failed to launch (based on a 'title' of \"Template\" being present after launching)")
        
        self.UTILS.goHome()
