#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_ftu
from gaiatest import GaiaTestCase

class test_27(GaiaTestCase):
    _Description = "First time use screens."
    
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 27)
        self.FTU        = app_ftu.main(self, self.testUtils)
        self.testUtils.reportError("roy")
        self.wifi_name = "TelefonicaFree"
        self.wifi_user = "roytest"
        self.wifi_pass = "roytest123"
        #self.wifi_name  = self.testUtils.get_os_variable("WIFI_TEST_27", "Name of wifi to connect to (case sensitive!)")
        #self.wifi_user  = self.testUtils.get_os_variable("USERNAME_27", "Wifi username")
        #self.wifi_pass  = self.testUtils.get_os_variable("PASSWORD_27", "Wifi password")
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Turn off all networking.
        #
        self.data_layer.disable_cell_data()
        self.data_layer.disable_wifi()
        
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Launch FTU app.
        #
        self.FTU.launch()

        #
        # In language, click "Englsh (US)".
        #
        self.wait_for_element_displayed(*DOM.FTU.language_list)
        #x = self.marionette.find_elements(*DOM.FTU.language_list)
        #for i in x:
            #self.testUtils.reportComment("X: " + i.text)
            
        x = self.testUtils.get_element("xpath", DOM.FTU.language_Sel_xpath % "English (US)")
        self.marionette.tap(x)
        
        #
        # Move on to the next screen.
        #
        x = self.testUtils.get_element(*DOM.FTU.next_button)
        self.marionette.tap(x)
        
        #
        # Enable data.
        # (crazy - the switch has an "id", but if you use that it never becomes 'visible'!)
        #
        self.wait_for_element_displayed(*DOM.FTU.section_cell_data)
        x = self.testUtils.get_element(*DOM.FTU.dataconn_switch)
        self.marionette.tap(x)

        #
        # Move on to the next screen.
        #
        x = self.testUtils.get_element(*DOM.FTU.next_button)
        self.marionette.tap(x)
        
        #
        # Wait for some networks to be found.
        #
        self.wait_for_condition(lambda m: len(m.find_elements(*DOM.FTU.wifi_networks_list)) > 0,
                                message="No networks listed on screen")
                                
        #
        # Pick the one we chose.
        #
        x= self.testUtils.get_element('id', self.wifi_name)
        self.marionette.tap(x)
        
        #
        # In case we are asked for a username and password ...
        #
        import time
        time.sleep(2)
        wifi_login_user = self.marionette.find_element(*DOM.FTU.wifi_login_user)
        wifi_login_pass = self.marionette.find_element(*DOM.FTU.wifi_login_pass)
        wifi_login_join = self.marionette.find_element(*DOM.FTU.wifi_login_join)
        if wifi_login_user.is_displayed():
            wifi_login_user.send_keys(self.wifi_user)
            wifi_login_pass.send_keys(self.wifi_pass)
            self.marionette.tap(wifi_login_join)
        
        #
        # Move on to the next screen.
        #
        x = self.testUtils.get_element(*DOM.FTU.next_button)
        self.marionette.tap(x)
        
        #
        # Change the continent.
        #
        self.wait_for_element_displayed('id', 'time-form')
        x = self.testUtils.get_element('xpath', ".//*[@id='time-form']/ul/li[1]/button")
        self.marionette.tap(x)
        self.testUtils.reportComment("BUTTON: " + x.text)
        #x.click()
        
        time.sleep(2)
        self.testUtils.savePageHTML("/tmp/roy1.html")

