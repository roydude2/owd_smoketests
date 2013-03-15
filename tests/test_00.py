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

class test_21(GaiaTestCase):
    _Description = "Get an app from the marketplace and run it."
    
    APP_NAME    = 'Wikipedia'
    APP_AUTHOR  = 'tfinc'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 21)
        self.Market     = AppMarket(self)
        self.Settings   = AppSettings(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.Market.launch()
        
        self.UTILS.goHome()
        
        self.UTILS.scrollHomescreenRight()
        
#        self.homescreen = self.apps.launch('Homescreen')
#        self.marionette.switch_to_frame()
#        x = self.homescreen.frame
#        self.UTILS.reportComment("src: " + x.get_attribute("src"))
#        self.UTILS.reportComment("id : " + x.get_attribute("id"))
#        self.marionette.switch_to_frame(self.homescreen.frame)
        


