#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings, app_browser
from gaiatest import GaiaTestCase

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
        self.testUtils  = TestUtils(self, 31)
        self.Settings   = app_settings.main(self, self.testUtils)
        self.Browser    = app_browser.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Uninstall the app (if need be).
        #
        try: self.apps.uninstall(self._appName)
        except: x=1 #(ignore any exceptions)
        
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Launch Settings app.
        #
        self.Settings.launch()
        
        self.Settings.cellular_and_data()
        
        #
        # Wifi needs to be off for this test to work.
        #
        self.Settings.turn_dataConn_on(True)
        
        self.testUtils.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is OFF! Please run this again (I currently cannot force it to be off before I toggle it).", True)
        
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
        # Install the app (these DOM items are peculiar to this little app,
        # so dont bother putting them in the main DOM.py file).
        #
        x = ('id', 'install-app')        
        install_btn = self.testUtils.get_element(*x)
        self.marionette.tap(install_btn)
        
        # Install button on the splash screen (switch to main frame to 'see' this).
        self.marionette.switch_to_frame()

        x = ('id', 'app-install-install-button')        
        install_btn = self.testUtils.get_element(*x)
        self.marionette.tap(install_btn)
        
        # ... and switch back to brwoser to see the next splash screen(!)
        self.testUtils.switchFrame(*DOM.Browser.frame_locator)
        x = ('id', 'modal-dialog-alert-ok')
        btn = self.testUtils.get_element(*x)
        self.marionette.tap(btn)

        #
        # Go back to the home page and check the app is installed.
        #
        self.testUtils.TEST(self.testUtils.isAppInstalled(self._appName), "App icon not found in homescreen.")
        
        self._appOk = True
        try: 
            self.apps.launch(self._appName)
        except:
            self._appOk = False
        
        self.testUtils.TEST(self._appOk, "App failed to launch.", True)

        #
        # Make sure the app launched (just check something from the app is 'there').
        #
        self._appOk = True
        try: 
            x = ('xpath', '//title[text()="Template"]')
            self.wait_for_element_present(*x)
        except:
            self._appOk = False
        
        self.testUtils.TEST(self._appOk, "App failed to launch (based on a 'title' of \"Template\" being present after launching)")
        
        self.testUtils.goHome()
