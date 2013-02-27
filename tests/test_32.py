#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings, app_browser
from gaiatest import GaiaTestCase

class test_32(GaiaTestCase):
    _Description = "Use Data Connection to download packaged app, then delete it."
    
    _URL         = "http://everlong.org/mozilla/packaged/"
    _appName     = "cool packaged app"
    _appOK       = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 32)
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
        # Install the app.
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
                
        #
        # Find the app icon.
        #
        self.testUtils.switchFrame(*DOM.GLOBAL.home_frame_locator)
        
        # Setup element object referencing our icon.
        app_xpath = ('xpath', DOM.GLOBAL.app_icon_str % "cool packaged app")
        app_icon = self.marionette.find_element(*app_xpath)
        
        self.testUtils.TEST(self.testUtils.findAppIcon(app_icon),
            "Could not find the app icon on the homescreen.", True)
        
        #
        # We found it! Go into edit mode (can't be done via marionette gestures yet).
        #
        self.testUtils.activateHomeEditMode()
        
        #
        # Delete it.
        #
        delete_button = app_icon.find_element(*DOM.GLOBAL.app_delete_icon)
        self.marionette.tap(delete_button)
 
        #
        # Confirm deletion.
        #
        self.wait_for_element_displayed(*DOM.GLOBAL.app_confirm_delete)
        delete = self.marionette.find_element(*DOM.GLOBAL.app_confirm_delete)
        self.marionette.tap(delete)

        #
        # Once it's gone, go home and check the icon is no longer there.
        #
        self.wait_for_element_not_present(*app_xpath)
        
        self.testUtils.touchHomeButton()
        self.testUtils.TEST(not self.testUtils.isAppInstalled(self._appName), "App is still installed after deletion.")
        
