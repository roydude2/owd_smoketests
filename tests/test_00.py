import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_contacts, app_settings
from tests.mock_data.contacts import MockContacts
from gaiatest import GaiaTestCase

class test_40(GaiaTestCase):
    _Description = "Importing facebook contacts."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 40)
        self.contacts   = app_contacts.main(self, self.UTILS)
        self.settings   = app_settings.main(self, self.UTILS)
                
        #
        # Set timeout for element searches.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1

        #
        # We're not testing adding a contact, so just stick one 
        # into the database.
        #
        self.data_layer.insert_contact(self.Contact_1)
        
        #
        # Set up to use data connection.
        #
        self.UTILS.reportError("roy")
        #self.settings.turn_dataConn_on(False)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Enable facebook.
        #
        self.contacts.enableFaceBook()
        
        #
        # Give facebook time to load, then connect to the iframe with src="".
        #
        import time
        time.sleep(8)

        self.marionette.switch_to_frame()
        self.UTILS.connect_to_iframe("")

        #
        # Login?
        #
        time.sleep(1)
        try:
            x = self.marionette.find_element(*DOM.Facebook.email)
            if x.is_displayed():
                x.send_keys("roytesterton.1@gmail.com")
                
                x = self.UTILS.get_element(*DOM.Facebook.password)
                x.send_keys("test123x")

                x = self.UTILS.get_element(*DOM.Facebook.login_button)
                self.marionette.tap(x)
        except:
            ignoreme=1
        
        #
        # Install?
        #
        time.sleep(1)
        try:
            x = self.marionette.find_element(*DOM.Facebook.install_fbowd_button)
            if x.is_displayed():
                self.marionette.tap(x)
        except:
            ignoreme=1
        
        time.sleep(6)
        self.marionette.switch_to_frame()
        self.UTILS.connect_to_iframe(DOM.Facebook.facebook_friends_iframe)
        
        x = self.marionette.find_elements("tag name", "button")
        for i in x:
            self.UTILS.reportError("BTN id " + i.get_attribute("id") + ", class '" + i.get_attribute("class") + ", text '" + i.text + "'")
        
        #time.sleep(1)
        #self.UTILS.savePageHTML("/tmp/roy1.html")

        ## FOR TEST 41 ...
        ##
        ## Select my contact.
        ##
        #self.contacts.viewContact(self.Contact_1)
        
        ##
        ## Tap link button to go to facebook.
        ##
        #self.contacts.tapLinkButton()
        
