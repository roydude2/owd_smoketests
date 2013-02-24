from apps import DOM
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.testUtils  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.app = self.parent.apps.launch('Settings')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    #
    # Open wifi settings.
    #
    def wifi(self):
        x = self.testUtils.get_element(*DOM.Settings.wifi)
        self.marionette.tap(x)
        self.parent.wait_for_element_displayed(*DOM.Settings.wifi_header)

    #
    # Click slider to turn wifi on.
    #
    def turn_wifi_on(self):
        if not self.parent.data_layer.get_setting("wifi.enabled"):
            x = self.testUtils.get_element(*DOM.Settings.wifi_enabled)
            self.marionette.tap(x)

    #
    # Verify the expected network is connected.
    #
    def checkWifiConnected(self, p_name):
        # 
        # Wait a little time to be sure the networks are all listed.
        #
        time.sleep(5)
        
        #
        # Compare the available networks - if one's connected then check it's the
        # one we expect (starts at array 3).
        #
        x = self.marionette.find_elements(*DOM.Settings.wifi_available_networks)
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
        

    #
    # Select a network.
    #
    def tap_wifi_network_name(self, p_wifi_name):
        self.testUtils.reportComment("ROY FIX THIS")
        #wifi_name_element = DOM.Settings.wifi_name_xpath % p_wifi_name
        #x= self.testUtils.get_element('xpath', wifi_name_element)
        #self.marionette.tap(x)
        
        #
        # Wait for 'anything' to be Connected.
        #
        try: 
            self.parent.wait_for_element_displayed(*DOM.Settings.wifi_connected)

        except:
            self.testUtils.reportError("Connected to '" + p_wifi_name + "' not established before timeout.")
            self.testUtils.quitTest()       

