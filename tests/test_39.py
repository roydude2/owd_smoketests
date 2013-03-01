#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings, app_everythingMe
from gaiatest import GaiaTestCase
import time

class test_00(GaiaTestCase):
    _Description = "Install an app via 'everything.me'."
    
    _APP_NAME    = "Tetris"
    _APP_ID      = "app_807"
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = TestUtils(self, 0)
        self.Settings   = app_settings.main(self, self.UTILS)
        self.EME        = app_everythingMe.main(self, self.UTILS)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.data_layer.disable_wifi()
        self.data_layer.disable_cell_data()
        
        #
        # Make sure our app isn't installed already.
        #
        try:
            if self.UTILS.isAppInstalled(self._APP_NAME):
                self.UTILS.uninstallApp(self._APP_NAME)
                
            self.UTILS.goHome()
            
            # Doesn't work for Tetris for some reason.
            #self.apps.uninstall(self._APP_NAME)
        except:
            ignoreme=1 # Do nothing.
            
        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.reportComment(
                "Couldn't automatically set Homescreen geolocation permission (problem with gaiatest script: \"self.apps.set_permission('Homescreen', 'geolocation', 'deny')\").")

    def tearDown(self):
        self.UTILS.reportResults()
        
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
        
        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.TEST(self.EME.launch(), "No application icons found.", True)
        
        #
        # Pick a group.
        # At the mercy of dev here - the word "Games" isn't in the html, so hopefully it will
        # always just be list item '1'.
        self.EME.pickGroup(1)
        
        # Again, at the mercy of dev - app names do not apear in the html dump, so
        # I have no choice but to assume this ID will always match our app.
        self.EME.addAppToHomescreen(self._APP_ID)
        
        #
        # Go back to the homescreen and check it's installed.
        #
        self.UTILS.goHome()
        self.UTILS.TEST(self.UTILS.isAppInstalled(self._APP_NAME), self._APP_NAME + " not installed.", True)
        self.UTILS.launchAppViaHomescreen(self._APP_NAME)
        
        #
        # Give it 10 seconds to start up, switch to the frame for it and grab a screenshot.
        #
        time.sleep(10)
        self.marionette.switch_to_frame()
        self.UTILS.connect_to_iframe("https://aduros.com/block-dream")
        x = self.UTILS.screenShot("_" + self._APP_NAME)
        self.UTILS.reportComment("NOTE: Please check the game screenshot in " + x)
