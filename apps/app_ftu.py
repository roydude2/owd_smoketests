import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppFTU(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):

        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS
            

    def launch(self):
        self.apps.kill_all()
        # We need WiFi enabled but not connected to a network
        self.data_layer.enable_wifi()
        self.data_layer.forget_all_networks()

        # Cell data must be off so we can switch it on again
        self.data_layer.disable_cell_data()

        self.app = self.apps.launch('FTU')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");

    def _select(self, match_string):
        #
        # Selects an item from a select box (lifted directly from gaiatest).
        #

        # Cheeky Select wrapper until Marionette has its own
        # Due to the way B2G wraps the app's select box we match on text
        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        #
        # This won't be around for too long hopefully, so just leave these
        # DOM defs here.
        #
        options = self.UTILS.getElements(('css selector', '#value-selector-container li'), "Item list", False, 20, False)
        close_button = self.UTILS.getElement(('css selector', 'button.value-option-confirm'), "Confirm selection button", False, 20, False)

        #
        # Is the scroller visible?
        #
        if len(options) > 0:
            # Loop options until we find the match
            for li in options:
                if li.text == match_string:
                    li.click()
                    break
    
            close_button.click()

        # Now back to app
        self.marionette.switch_to_frame(self.app.frame)

    def setLanguage(self, p_lang):
        time.sleep(1)
        x = self.UTILS.getElements(DOM.FTU.language_list, "Language list", True, 20, False)
        
        if len(x) > 0:
            for i in x:
                if i.text == p_lang:
                    self.marionette.tap(i)
                    return True
        
        return False
        
    def nextScreen(self):
        #
        # Click to the next screen (works until you get to the tour).
        #
        x = self.UTILS.getElement(DOM.FTU.next_button, "Next button")
        self.marionette.tap(x)
        time.sleep(1)
        
    def startTour(self):
        #
        # Click to start the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_start_btn, "Start tour button")
        self.marionette.tap(x)
        time.sleep(1)

    def skipTour(self):
        #
        # Click to skip the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_skip_btn, "Skipt tour button")
        self.marionette.tap(x)
        time.sleep(1)

    def nextTourScreen(self):
        #
        # Click to next page of the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_next_btn, "Tour 'next' button")
        self.marionette.tap(x)
        time.sleep(1)

    def endTour(self):
        #
        # Click to end the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_finished_btn, "Finish tour button")
        self.marionette.tap(x)
        time.sleep(1)

    def setDataConnEnabled(self):
        #
        # Enable data.
        # (the switch has an "id", but if you use that it never becomes 'visible'!)
        #
        self.UTILS.waitForElements(DOM.FTU.section_cell_data, "Cellular data connection section")

        x = self.UTILS.getElement(DOM.FTU.dataconn_switch, "Data connection switch")
        self.marionette.tap(x)
        
        # Wait a moment, then check data conn is on.
        time.sleep(3)
        self.UTILS.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is enabled after trying to enable it.", True)
        
    def setNetwork(self, p_wifiName, p_userName, p_password):
        #
        # Join a wifi network.
        #
        time.sleep(5)
        x = self.UTILS.getElements(DOM.FTU.wifi_networks_list, "Wifi network list")

        #
        # Pick the one we chose.
        #
        x= self.UTILS.getElement(('id', p_wifiName), "Wifi network '" + p_wifiName + "'")
        self.marionette.tap(x)
            
        #
        # In case we are asked for a username and password ...
        #
        time.sleep(2)
        wifi_login_user = self.marionette.find_element(*DOM.FTU.wifi_login_user)
        if wifi_login_user.is_displayed():
            wifi_login_pass = self.marionette.find_element(*DOM.FTU.wifi_login_pass)
            wifi_login_join = self.marionette.find_element(*DOM.FTU.wifi_login_join)
            wifi_login_user.send_keys(p_userName)
            wifi_login_pass.send_keys(p_password)
            self.marionette.tap(wifi_login_join)
        
    def setTimezone(self, p_continent, p_city):
        
        #
        # Set the timezone.
        #
        self.UTILS.waitForElements(DOM.FTU.timezone, "Timezone area")

        continent_select = self.UTILS.getElement(DOM.FTU.timezone_continent, "Continent button", False)
        continent_select.click() # Must be 'clicked' not 'tapped'
        self._select(p_continent)

        city_select = self.UTILS.getElement(DOM.FTU.timezone_city, "City button", False)
        city_select.click() # Must be 'clicked' not 'tapped'
        self._select(p_city)

        self.UTILS.TEST(
            p_continent + "/" + p_city in self.UTILS.getElement(DOM.FTU.timezone_title, "Timezone title").text,
            "Locality is set up correctly")
