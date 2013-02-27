#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings, app_browser
from gaiatest import GaiaTestCase

class test_17(GaiaTestCase):
    _Description = "Use Data Connection."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 17)
        self.Settings   = app_settings.main(self, self.testUtils)
        self.Browser    = app_browser.main(self, self.testUtils)
        self.testURL    = self.testUtils.get_os_variable("URL_TEST_17", "URL to test data connection with")
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        self.testUtils.reportComment("Using " + self.testURL)
        
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
        
        #
        # Open the browser app.
        #
        self.Browser.launch()
        
        #
        # Open our URL.
        #
        self.Browser.open_url(self.testURL)

        #
        # Check the page didn't have a problem.
        #
        self.Browser.check_page_loaded()
        

