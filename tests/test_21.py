import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_market
from gaiatest import GaiaTestCase

class test_21(GaiaTestCase):
    _Description = "Get an app from the marketplace and run it."
    
    APP_NAME = 'Wikipedia'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 21)
        self.Market     = app_market.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        self.testUtils.reportComment("Using app '" + self.APP_NAME + "'")
        
        #
        # Make sure our app isn't installed already.
        #
        try:
            self.apps.uninstall(self.APP_NAME)
        except:
            x=1 # Do nothing.
        
    def tearDown(self):
        self.testUtils.reportResults()
        
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
        self.testUtils.goHome()
        
        self.app = self.apps.launch(self.APP_NAME)
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)
        
        test_title = ('class name', 'titlebarIcon')
        self.wait_for_element_displayed(*test_title)
        x = self.marionette.find_element(*test_title)
        self.testUtils.TEST(x.get_attribute("title") == "Wikipedia homepage",
            "Application did not have the expected title - please check the screenshot matches '" + self.APP_NAME  + "'")
        
