#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from utils      import UTILS
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_settings import *
from apps.app_browser import *

class test_16(GaiaTestCase):
    _Description = "Load a website via Wifi."
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = AppSettings(self)
        self.Browser    = AppBrowser(self)
        self.wifi_name  = self.UTILS.get_os_variable("WIFI_TEST_16", "Name of wifi to connect to (case sensitive!)")
        self.testURL    = self.UTILS.get_os_variable("URL_TEST_16", "URL to test wifi with")
        self.wifi_user  = self.UTILS.get_os_variable("USERNAME_16", "Wifi username")
        self.wifi_pass  = self.UTILS.get_os_variable("PASSWORD_16", "Wifi password")

        self.marionette.set_search_timeout(50)
        
        self.data_layer.disable_wifi()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
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
        self.UTILS.TEST(
                self.Settings.checkWifiLisetedAsConnected(self.wifi_name),
                "Wifi '" + self.wifi_name + "' is listed as 'connected' in wifi settings.", True)
            
        #
        # Open the browser app.
        #
        self.Browser.launch()
        
        #
        # Open our URL.
        #
        self.Browser.open_url(self.testURL)

        
        
        
        

