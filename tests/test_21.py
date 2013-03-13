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
from apps.app_market import *
from apps.app_settings import *

class test_21(GaiaTestCase):
    _Description = "Get an app from the marketplace and run it."
    
    APP_NAME = 'Wikipedia'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 21)
        self.Market = AppMarket(self)
        self.Settings   = AppSettings(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Ensure we have a connection.
        #
        self.Settings.trun_dataConn_on_if_required()
        
        self.UTILS.reportComment("Using app '" + self.APP_NAME + "'")
        
        #
        # Make sure our app isn't installed already.
        #
        try:
            self.apps.uninstall(self.APP_NAME)
        except:
            pass # Do nothing.
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch market app.
        #
        self.Market.launch()
        
        #
        # Install app.
        # NOTE: At the moment this just installs the first app it finds (Wikipedia)!
        # Once marionette gestures are fixed (or someone removes that slider that reveals the
        # search box) then fix this.
        self.Market.install_app(self.APP_NAME)


        #
        # Verify installation.
        #
        self.Market.verify_app_installed(self.APP_NAME)
        
        #
        # Go home then run the new app.
        #
        self.UTILS.goHome()
        
        self.app = self.apps.launch(self.APP_NAME)
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.GLOBAL.app_titlebar_name", 20))
        x = self.marionette.find_element(*self.UTILS.verify("DOM.GLOBAL.app_titlebar_name"))
        self.UTILS.TEST(x.get_attribute("title") == "Wikipedia homepage",
            "Application did not have the expected title - please check the screenshot matches '" + self.APP_NAME  + "'")
        
