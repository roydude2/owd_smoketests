import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
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
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS



    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Settings')
        self.UTILS.waitForNotDisplayed(20, "Loading overlay stops being displayed", False, DOM.GLOBAL.loading_overlay);

    def wifi(self):
        #
        # Open wifi settings.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Settings.wifi"))
        self.marionette.tap(x)
        
        self.UTILS.waitForDisplayed(20, "Wifi header appears.", False, self.UTILS.verify("DOM.Settings.wifi_header"))
#        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Settings.wifi_header"))

    def cellular_and_data(self):
        #
        # Open cellular and data settings.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Settings.cellData"))
        self.marionette.tap(x)
        
        self.UTILS.waitForDisplayed(20, "Celldata header appears.", False, self.UTILS.verify("DOM.Settings.celldata_header"))
#        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Settings.celldata_header"))

    def turn_dataConn_on_if_required(self):
        #
        # Turns data conn on via settings app, but only
        # if it's not already on.
        #
        if not self.data_layer.get_setting("ril.data.enabled"):
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
            
            x = self.UTILS.get_element(*self.UTILS.verify("DOM.Settings.celldata_DataConn"))
            self.marionette.tap(x)
            
        #
        # If we get prompted for action, say 'Turn ON'.
        #
        # (Because it's only 'if', we don't verfy this DOM setting.)
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
            "Data connection is enabled after trying to enable it.", True)
        
        #
        # Give the statusbar icon time to appear, then check for it.
        #
        # NOTE: 'p_wifiOFF' works here: if it's true then the icon SHOULD be there, else
        #       it shouldn't.
        #
        if p_wifiOFF:
            x = self.UTILS.check_statusbar_for_icon(DOM.Statusbar.dataConn, DOM.Settings.frame_locator)
            self.UTILS.TEST(x, 
                            "Data connection icon is present in the status bar.", 
                            True)


    def turn_wifi_on(self):
        #
        # Click slider to turn wifi on.
        #
        if not self.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.get_element(*self.UTILS.verify("DOM.Settings.wifi_enabled"))
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
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Settings.wifi_available_networks"))
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
        x= self.UTILS.get_element('xpath', wifi_name_element)
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
        wifi_login_pass = self.marionette.find_element(*self.UTILS.verify("DOM.Settings.wifi_login_pass"))
        wifi_login_ok   = self.marionette.find_element(*self.UTILS.verify("DOM.Settings.wifi_login_ok_btn"))
        if wifi_login_user.is_displayed():
            wifi_login_user.send_keys(p_user)
            wifi_login_pass.send_keys(p_pass)
            self.marionette.tap(wifi_login_ok)
        else:
            #
            # We were not asked, so go back to the list.
            #
            backBTN = self.UTILS.get_element(*self.UTILS.verify("DOM.Settings.back_button"))
            self.marionette.tap(backBTN)
#            self.wait_for_element_displayed('xpath', DOM.GLOBAL.app_head_specific % "Wi-Fi")
            self.UTILS.TEST(self.UTILS.headerCheck("Wi-Fi"), "Header is 'Wi-Fi'.")
        
        #
        # A couple of checks to wait for 'anything' to be Connected.
        #
#        conBool = False
#        try:
        self.UTILS.waitForDisplayed(20, "Wifi is marked 'connected' in the list.", False, self.UTILS.verify("DOM.Settings.wifi_connected"))
#            self.wait_for_element_displayed(*self.UTILS.verify("DOM.Settings.wifi_connected"))
#            conBool = True
#        except:
#            conBool = False
#        self.UTILS.TEST(conBool, "Wifi is marked as 'Connected' in the list.")
        
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
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Settings.sound"))
        self.marionette.tap(x)
