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
        self.wifi_user  = self.testUtils.get_os_variable("USERNAME_16", "Wifi username")
        self.wifi_pass  = self.testUtils.get_os_variable("PASSWORD_16", "Wifi password")

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
        # Connect to the wifi.
        #
        self.Settings.tap_wifi_network_name(self.wifi_name, self.wifi_user, self.wifi_pass)
        
        #
        # Tap specific wifi network (if it's not already connected).
        #
        self.testUtils.TEST(
                self.Settings.checkWifiLisetedAsConnected(self.wifi_name),
                "Wifi '" + self.wifi_name + "' not listed as 'connected' in wifi settings.", True)
            
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
        
        
        

