import sys
sys.path.insert(1, "./")
from tools import TestUtils

from gaiatest import GaiaTestCase
import time

class test_1(GaiaTestCase):
    
    _Contact1 = {
        "givenName" : "John",
        "familyName": "Smith",
        "name"      : "John Smith",
        "email"     : {"type": "", "value": "john.smith@nowhere.com"},
        "tel"       : {"type": "Mobile", "value": "111111111"},
        "adr"       : {"streetAddress"    : "One Street",
                       "postalCode"       : "00001",
                       "locality"      : "City One",
                       "countryName"   : "Country One"},
        "bday"      : "1981-01-21",
        "jobTitle"  : "Runner number one",
        "comment"   : "Mock test contact 1"
    }

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.data_layer.insert_contact(self._Contact1)
        self.UTILS      = TestUtils(self, 41)
            
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.apps.launch("Contacts")
        
        #
        # Open our contact (just click the first one we come across).
        #
        x = self.marionette.find_elements("xpath", "//li[@class='contact-item']")
        self.marionette.tap(x[0])
        time.sleep(2)
        
        #
        # Click the 'Link contact' button.
        #
        # NOTE: At this point there at 2 buttons with the
        #       id "link_button", so make sure you're using
        #       the displayed one!
        #
        x = self.marionette.find_elements('id', "link_button")
        for i in x:
            if i.is_displayed():
                self.marionette.tap(i)
                break
        
        time.sleep(5)
        
        #
        # Travel through the frames to the one we need for the fb import page.
        #
        self.marionette.switch_to_frame()
        time.sleep(2)

        x = self.marionette.find_element(
            'css selector', 
            'iframe[src="app://communications.gaiamobile.org/contacts/index.html"]'
            )
        self.marionette.switch_to_frame(x)        
        time.sleep(2)
        
        x = self.marionette.find_element(
            'id', 
            'fb-extensions'
            )
        self.marionette.switch_to_frame(x)        
        time.sleep(2)

        #
        # Wait for the fb friends page to start.
        #
        self.wait_for_element_displayed(
            'xpath', 
            "//h1[text()='Facebook Friends']")
        time.sleep(2)
        
        #
        # Select a contact from the list
        #
        x = self.marionette.find_element("xpath", "//*[@id='friends-list']//li[1]")
        
        if x.is_displayed():
            print "YES!"
            self.marionette.tap(x)
        
        