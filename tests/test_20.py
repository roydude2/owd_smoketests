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
from marionette.keys import Keys

class test_20(GaiaTestCase):
    _Description = "Get an app from the marketplace."
    
    APP_NAME    = 'Wikipedia'
    APP_AUTHOR  = 'tfinc'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 20)
        self.Market     = AppMarket(self)
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
        # Install our app.
        #
        self.UTILS.TEST(self.Market.install_app(self.APP_NAME, self.APP_AUTHOR),
                        "Failed to install app.", True)
        
        #
        # Verify installation.
        #
        self.Market.verify_app_installed(self.APP_NAME)
        
        #
        # Find the app icon (a nice touch! :o).
        #
        self.UTILS.TEST(self.UTILS.findAppIcon(self.APP_NAME),
                        "Unable to find app '" + self.APP_NAME + "' on the homescreen!")

