#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from marionette.keys import Keys

class test_20(GaiaTestCase):
    _Description = "Install a market installed hosted app."
    
    APP_NAME    = 'Wikipedia'
    APP_AUTHOR  = 'tfinc'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Market     = AppMarket(self)
        self.Settings   = AppSettings(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Ensure we have a connection.
        #
        self.Settings.turn_dataConn_on_if_required()
        
        self.UTILS.logComment("Using app '" + self.APP_NAME + "'")
        
        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.uninstallApp(self.APP_NAME)
        
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
                        "Successfully installed application '" + self.APP_NAME + "'.", True)

        
        #
        # Find the app icon on the homescreen.
        #
        self.UTILS.TEST(self.UTILS.findAppIcon(self.APP_NAME),
                        "Application '" + self.APP_NAME + "' is present on the homescreen.")

