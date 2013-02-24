import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings, app_browser
from gaiatest import GaiaTestCase

class test_16(GaiaTestCase):
    _Description = "Connect to Wifi network."
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 16)
        self.Settings   = app_settings.main(self, self.testUtils)
        self.Browser    = app_browser.main(self, self.testUtils)
        self.wifi_name  = self.testUtils.get_os_variable("WIFI_TEST_16", "Name of wifi to connect to (case sensitive!)")
        self.testURL    = self.testUtils.get_os_variable("URL_TEST_16", "URL to test wifi with")

        self.marionette.set_search_timeout(50)
        
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        #
        # Forget all networks (so we have to chose one).
        # Roy- *might* want this, but if we're already connected then this is a 'pass' anyway.
        #self.data_layer.forget_all_networks()
        
        #
        # Open the Settings application.
        #
        self.Settings.launch()
        
        #
        # Tap Wi-Fi.
        #
        self.Settings.wifi()

        #
        # Make sure wifi is set to 'on'.
        #
        self.Settings.turn_wifi_on()
        
        #
        # Tap specific wifi network (if it's not already connected).
        #
        self.testUtils.reportComment("Using network \"" + self.wifi_name + "\".")
        if self.Settings.checkWifiConnected(self.wifi_name):
            self.testUtils.reportComment("\"" + self.wifi_name + "\" is already connected.")
        else:
            self.Settings.tap_wifi_network_name(self.wifi_name)
            self.testUtils.TEST(
                self.Settings.checkWifiConnected(self.wifi_name),
                "Unable to connect to '" + self.wifi_name + "'", True)
            
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
        
        
        

