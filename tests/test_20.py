import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_market
from gaiatest import GaiaTestCase

class test_20(GaiaTestCase):
    _Description = "Get an app from the marketplace."
    
    APP_NAME = 'Wikipedia'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 20)
        self.Market   = app_market.main(self, self.UTILS)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
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
        #
        self.Market.install_app(self.APP_NAME)

        #
        # Verify installation.
        #
        self.Market.verify_app_installed(self.APP_NAME)
        
        #
        # Find the app icon (a nice touch! :o).
        #
        myApp = self.UTILS.findAppIcon(self.APP_NAME)
        self.UTILS.TEST(myApp,
            "Could not find the app icon on the homescreen.", True)
