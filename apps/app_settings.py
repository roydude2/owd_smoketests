import DOM, time
from gaiatest   import GaiaTestCase
from utils      import UTILS
from marionette import Marionette

class AppSettings(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = UTILS(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS



    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Settings')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");

    def cellular_and_data(self):
        #
        # Open cellular and data settings.
        #
        x = self.UTILS.getElement(DOM.Settings.cellData, "Cellular and Data settings link")
        self.marionette.tap(x)
        
        self.UTILS.waitForElements(DOM.Settings.celldata_header, "Celldata header", True, 20, False)

    def turn_dataConn_on_if_required(self):
        #
        # Turns data conn on via settings app, but only
        # if it's not already on.
        #
#        if not self.data_layer.get_setting("ril.data.enabled")
        x = self.UTILS.isIconInStatusBar(DOM.Statusbar.dataConn)
        if not x:
            self.turn_dataConn_on()

    def turn_dataConn_on(self, p_wifiOFF=False):
        #
        # Click slider to turn data connection on.
        #

        #
        # First, make sure we're in "Settings".
        #
        try:
            x = self.marionette.find_element(*DOM.Settings.frame_locator)
        except:
            #
            # Settings isn't running, so start it.
            #
            self.launch()
            self.cellular_and_data()
        
        if p_wifiOFF:
            if self.data_layer.get_setting("wifi.enabled"):
                self.data_layer.disable_wifi()
            
        time.sleep(1)
        
        if not self.data_layer.get_setting("ril.data.enabled"):
            #
            # If we disabled the wifi we'll be in the wrong frame here, so just make sure ...
            #
            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Settings.frame_locator)
            
            x = self.UTILS.getElement(DOM.Settings.celldata_DataConn, "Connect to cellular and data link")
            self.marionette.tap(x)
            
        #
        # If we get prompted for action, say 'Turn ON'.
        #
        # (Because it's only 'if', we don't verfy this element.)
        #
        time.sleep(2)
        try:
            x = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            if x.is_displayed():
                self.marionette.tap(x)
        except:
            pass

        #
        # Give it time to start up.
        #
        time.sleep(5)
        
        #
        # Check to see if data conn is now enabled (it may be, even if the icon doesn't appear).
        #
        self.UTILS.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is enabled", True)
        
        #
        # Give the statusbar icon time to appear, then check for it.
        #
        # NOTE: 'p_wifiOFF' works here: if it's true then the icon SHOULD be there, else
        #       it shouldn't.
        #
        if p_wifiOFF:
            x = self.UTILS.isIconInStatusBar(DOM.Statusbar.dataConn, DOM.Settings.frame_locator)
            self.UTILS.TEST(x, 
                            "Data connection icon is present in the status bar.", 
                            True)
        
        self.UTILS.goHome()


    def wifi(self):
        #
        # Open wifi settings.
        #
        x = self.UTILS.getElement(DOM.Settings.wifi, "Wifi settings link")
        self.marionette.tap(x)
        
        self.UTILS.waitForElements(DOM.Settings.wifi_header, "Wifi header appears.", True, 20, False)

    def turn_wifi_on(self):
        #
        # Click slider to turn wifi on.
        #
        if not self.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.getElement(DOM.Settings.wifi_enabled, "Enable wifi switch")
            self.marionette.tap(x)
        
        #
        # Nothing to check for yet, because the network may require login etc...,
        # so just wait a little while before proceeding ...
        #
        time.sleep(3)
        
    def checkWifiLisetedAsConnected(self, p_name):
        #
        # Verify the expected network is listed as connected in 'available networks'.
        #

        # 
        # Wait a little time to be sure the networks are all listed.
        #
        time.sleep(5)
        
        #
        # Compare the available networks - if one's connected then check it's the
        # one we expect (starts at array 3).
        #
        x = self.UTILS.getElements(DOM.Settings.wifi_available_networks, "Available networks list", False, 20, False)
        for i in range(3, len(x)):
            connStatus = self.marionette.find_element('xpath', DOM.Settings.wifi_available_status % i)
            connName   = self.marionette.find_element('xpath', DOM.Settings.wifi_available_name   % i)
            
            if ("Connected" in connStatus.text) and (p_name == connName.text):
                return True
            else:
                return False
        #
        # If we get to here, we didn't find the network we were looking for.
        #
        return False
        
    def tap_wifi_network_name(self, p_wifi_name, p_user, p_pass):
        #
        # Select a network.
        #
        wifi_name_element = DOM.Settings.wifi_name_xpath % p_wifi_name
        x= self.UTILS.getElement(('xpath', wifi_name_element), "Wifi '" + p_wifi_name + "'", True, 10, True)
        if x:
            self.marionette.tap(x)
            return True
        else:
            return False
        
        #
        # In case we are asked for a username and password ...
        #
        time.sleep(2)
        wifi_login_user = self.marionette.find_element(*self.UTILS.verify("DOM.Settings.wifi_login_user"))
        if wifi_login_user.is_displayed():
            wifi_login_pass = self.marionette.find_element(*self.UTILS.verify("DOM.Settings.wifi_login_pass"))
            wifi_login_ok   = self.marionette.find_element(*self.UTILS.verify("DOM.Settings.wifi_login_ok_btn"))
            wifi_login_user.send_keys(p_user)
            wifi_login_pass.send_keys(p_pass)
            self.marionette.tap(wifi_login_ok)
        else:
            #
            # We were not asked, so go back to the list.
            #
            backBTN = self.UTILS.getElement(DOM.Settings.back_button, "Back button")
            self.marionette.tap(backBTN)

            self.UTILS.TEST(self.UTILS.headerCheck("Wi-Fi"), "Header is 'Wi-Fi'.")
        
        #
        # A couple of checks to wait for 'anything' to be Connected.
        #
        self.UTILS.waitForElements(DOM.Settings.wifi_connected, "Whichever Wifi network is connected", True, 20, False)
        
        self.UTILS.TEST(self.data_layer.get_setting("wifi.enabled"),
            "Wifi connection to '" + p_wifi_name + "' not established.", True)

    def setAlarmVolume(self, p_vol):
        #
        # Set the volume for alarms.
        #
        self.data_layer.set_setting('audio.volume.alarm', p_vol)
        
    def setRingerAndNotifsVolume(self, p_vol):
        #
        # Set the volume for ringer and notifications.
        #
        self.data_layer.set_setting('audio.volume.notification', p_vol)
        
    def goSound(self):
        #
        # Go to Sound menu.
        #
        self.launch()
        x = self.UTILS.getElement(DOM.Settings.sound, "Sound setting link")
        self.marionette.tap(x)


    def _getPickerSpinnerElement(self, p_DOM, p_msg):
        #
        # Returns the element for the spinner in a picker
        # (done this way because we need to figure out which one is
        # visible and it was getting messy repeating this!).
        # 
        # Get the elements that match this one.
        els = self.UTILS.getElements(p_DOM, p_msg, False, 20, True)
        
        # Get the one that's not hidden (the 'hidden'
        # attribute here has no 'value', so we need to just
        # check if it's been set to "".
        boolOK = False
        el     = False
        for i in els:
            if str(i.get_attribute("hidden")) == "false":
                boolOK = True
                el = i
                break
        
        self.UTILS.TEST(boolOK, "... one of them is visible|('hidden' attribute is not set)", True)
        return el

    def setTimeToNow(self):
        #
        # Set date and time to 'now'.
        # DOES NOT WORK YET (marionette.flick() not working here)!!
        self.launch()
        
        x = ("id", "menuItem-dateAndTime")
        el = self.UTILS.getElement(x, "Date & Time setting")
        self.marionette.tap(el)
        
        x = ("id", "clock-date")
        el = self.UTILS.getElement(x, "Date setting")
        el.click()
        
        time.sleep(2)        
        self.marionette.switch_to_frame()
        
        x = ("class name", "value-picker-date animation-on")
        eld = self._getPickerSpinnerElement(x, "Day spinners in date picker")
                
        x_pos   = eld.size['width']  / 2
        y_start = eld.size['height'] / 2
        y_end   = y_start * 0.2

        self.marionette.flick(eld, x_pos, y_start, x_pos, y_end, 270)
        