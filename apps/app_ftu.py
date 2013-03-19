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
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)


    #
    # Selects an item from a select box (lifted directly from gaiatest).
    #
    def _select(self, match_string):
        # Cheeky Select wrapper until Marionette has its own
        # Due to the way B2G wraps the app's select box we match on text
        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        #
        # This won't be around for too long hopefully, so just leave these
        # DOM defs here.
        #
        options = self.marionette.find_elements('css selector', '#value-selector-container li')
        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        #
        # Is the scroller visible?
        #
        if len(options) <= 0:
            self.UTILS.logResult(False, "The '" + match_string + "' scroller is displayed when the button is tapped.")
        else:
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
        x = self.UTILS.get_elements(*self.UTILS.verify("DOM.FTU.language_list"))
        self.UTILS.TEST(len(x) > 0, "SOME languages are listed.")
        
        for i in x:
            if i.text == p_lang:
                self.marionette.tap(i)
                return True
        
        return False
        
    #
    # Click to the next screen (works until you get to the tour).
    #
    def nextScreen(self):
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.FTU.next_button"))
        self.marionette.tap(x)
        time.sleep(1)
        
    #
    # Click to start the Tour.
    #
    def startTour(self):
        x = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.tour_start_btn"))
        self.marionette.tap(x)
        time.sleep(1)

    #
    # Click to skip the Tour.
    #
    def skipTour(self):
        x = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.tour_skip_btn"))
        self.marionette.tap(x)
        time.sleep(1)

    #
    # Click to next page of the Tour.
    #
    def nextTourScreen(self):
        x = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.tour_next_btn"))
        self.marionette.tap(x)
        time.sleep(1)

    #
    # Click to end the Tour.
    #
    def endTour(self):
        x = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.tour_finished_btn"))
        self.marionette.tap(x)
        time.sleep(1)

    #
    # Enable data.
    # (crazy - the switch has an "id", but if you use that it never becomes 'visible'!)
    #
    def setDataConnEnabled(self):
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.FTU.section_cell_data"))
        x = self.UTILS.get_element(*DOM.FTU.dataconn_switch)
        self.marionette.tap(x)
        
        # Wait a moment, then check data conn is on.
        time.sleep(3)
        self.UTILS.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is enabled after trying to enable it.", True)
        
    #
    # Join a wifi network.
    #
    def setNetwork(self, p_wifiName, p_userName, p_password):
        time.sleep(5)
        try:
            x = self.marionette.find_elements(*self.UTILS.verify("DOM.FTU.wifi_networks_list"))
        except:
            self.UTILS.logResult(False, "SOME networks are found in wifi screen.")
        else:
            self.UTILS.logComment("(Found " + str(len(x)) + " wifi networks.)")
            
            #
            # Pick the one we chose.
            #
            try:
                x= self.UTILS.get_element('id', p_wifiName)
            except:
                self.UTILS.logResult(False, "Wifi network '" + p_wifiName + "' is found.")
            else:
                self.marionette.tap(x)
                
                #
                # In case we are asked for a username and password ...
                #
                time.sleep(2)
                wifi_login_user = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.wifi_login_user"))
                wifi_login_pass = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.wifi_login_pass"))
                wifi_login_join = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.wifi_login_join"))
                if wifi_login_user.is_displayed():
                    wifi_login_user.send_keys(p_userName)
                    wifi_login_pass.send_keys(p_password)
                    self.marionette.tap(wifi_login_join)
        
    #
    # Set the timezone.
    #
    def setTimezone(self, p_continent, p_city):
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.FTU.timezone"))
        continent_select = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.timezone_continent"))
        # Click to activate the b2g select element
        continent_select.click()
        self._select(p_continent)

        city_select = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.timezone_city"))
        # Click to activate the b2g select element
        city_select.click()
        self._select(p_city)

        self.UTILS.TEST(
            p_continent + "/" + p_city in self.marionette.find_element(*self.UTILS.verify("DOM.FTU.timezone_title")).text,
            "Locality is set up correctly")
