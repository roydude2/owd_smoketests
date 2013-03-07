import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_contacts, app_settings
from tests.mock_data.contacts import MockContacts
from gaiatest import GaiaTestCase
import time

class test_41(GaiaTestCase):
    _Description = "Importing facebook contacts."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 41)
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
        # Set up to use data connection.
        #
        self.data_layer.disable_wifi()
        self.settings.turn_dataConn_on(False)
        
        #
        # You must be logged into facebook already to run this test
        # (cannot automated this because it requires a 'captcha').
        # So prompt for it before starting.
        #
        ignoreme = self.UTILS.get_os_variable("ENTER", "For test 41 please ensure you are logged into facebook on the device, then press")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Create new contact.
        #
        self.contacts.createNewContact(self.Contact_1)

        #
        # View the contact details.
        #
        self.contacts.viewContact(self.Contact_1)
        
        #
        # Press the link button.
        #
        self.contacts.pressLinkContact()

        #
        # Need to figure out a better way to do this.
        #
        x = self.marionette.find_elements("xpath", "//*[@id='friends-list']//li")
        
        fb_email = False
        
        for i in x:
            if i.is_displayed():
                #
                # Keep the name and email detais for this contact.
                #
                y = i.find_elements("tag name", "p")
                fb_email = y[1].text
                
                self.marionette.tap(i)
                break

        self.UTILS.TEST(fb_email, "Could not find linked contact's email address.")
        
        if fb_email:
            self.UTILS.reportComment("Linked FB contact email: " + fb_email + ".")
        
        #
        # Switch back and wait for contact details page to re-appear.
        #
        self.marionette.switch_to_frame()
        self.UTILS.connect_to_iframe(DOM.Facebook.fb_friends_iframe_1)
        x = self.UTILS.get_element("xpath", DOM.GLOBAL.app_head_specific % self.Contact_1['name'])

        #
        # Reload the contacts app (we need a little sleep to let the facebook
        # icon appear).
        #
        self.apps.kill_all()
        self.contacts.launch()
        time.sleep(2)

        #
        # Check that our contact is now listed as a facebook contact (icon by the name in 'all contacts' screen).
        #
        x = self.marionette.find_elements(*DOM.Contacts.view_all_fb_contacts)
        self.UTILS.TEST(len(x) > 0, "Our contact is not listed as a facebook contact after linking.")
        

        #
        # View the details for this contact.
        #
        self.contacts.viewContact(self.Contact_1)
        
        
        #
        # Check the expected elements are now visible. 
        #
        # I'm having serious problems finding buttons based on 'text' directly, so here's
        # the 'brute-force' method ...
        boolViewFbProfile   = False
        boolWallpost        = False
        boolLinkedEmail     = False
        boolUnLink          = False
        x = self.marionette.find_elements("tag name", "button")
        for i in x:
            if i.text == "View Facebook profile": boolViewFbProfile = True
            if i.text == "Wall post"            : boolWallPost      = True
            if i.text == fb_email               : boolLinkedEmail   = True
            if i.text == "Unlink contact"       : boolUnLink        = True
            
        self.UTILS.TEST(boolViewFbProfile   , "'View Facebook profile' button not displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolWallPost        , "'Wall post' button not displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolUnLink          , "'Unlink contact' button not displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolLinkedEmail     , "Linked facebook email address not displayed after contact linked to fb contact.")
        
