#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from tools      import TestUtils
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_contacts import *
from apps.app_facebook import *
from apps.app_settings import *
from tests.mock_data.contacts import MockContacts
import time

class test_41(GaiaTestCase):
    _Description = "Link a facebook contact."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self)
        self.contacts   = AppContacts(self)
        self.facebook   = AppFacebook(self)
        self.settings   = AppSettings(self)
                
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
        self.UTILS.logComment("Not disabling wifi at the moment")
#        self.data_layer.disable_wifi()
        self.settings.turn_dataConn_on_if_required()
        
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
        self.contacts.tapLinkContact()

        #
        # Select the contact to link.
        #
        fb_email = self.UTILS.get_os_variable("LINK_EMAIL_ADDRESS", "Email address of facebook account to link.")
        self.facebook.LinkContact(fb_email)
        
        #
        # Check we're back at our contact.
        #
        self.UTILS.TEST(self.UTILS.headerCheck(self.Contact_1['name']), 
                        "Header is '"+ self.Contact_1['name'] +"'.")

        #
        # This was covering up an error - these details should be available before
        # the contacts app is reloaded. 
#        #
#        # Reload the contacts app (we need a little sleep to let the facebook
#        # icon appear).
#        #
#        self.apps.kill_all()
#        self.contacts.launch()
#        time.sleep(2)

        #
        # Check that our contact is now listed as a facebook contact (icon by the name in 'all contacts' screen).
        #
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Contacts.social_network_contacts"))
        self.UTILS.TEST(len(x) > 0, "Contact is listed as a facebook contact after linking.")
        

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
            
        self.UTILS.TEST(boolViewFbProfile   , "'View Facebook profile' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolWallPost        , "'Wall post' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolUnLink          , "'Unlink contact' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolLinkedEmail     , "Linked facebook email address is displayed after contact linked to fb contact.")
        
