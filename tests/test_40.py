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

class test_40(GaiaTestCase):
    _Description = "Import Facebook contacts from contacts app settings."

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
        # We're not testing adding a contact, so just stick one 
        # into the database.
        #
        self.data_layer.insert_contact(self.Contact_1)
        
        #
        # Set up to use data connection.
        #
        self.data_layer.disable_wifi()
        self.settings.turn_dataConn_on_if_required()
        
        #
        # You must be logged into facebook already to run this test
        # (cannot automated this because it requires a 'captcha').
        # So prompt for it before starting.
        #
        ignoreme = self.UTILS.get_os_variable("ENTER", "For test 40 please ensure you are logged into facebook on the device, then press")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Enable facebook and log in.
        #
        self.contacts.enableFBImport()
        fb_user = self.UTILS.get_os_variable("FB_USERNAME", "Username to connect you to facebook.")
        fb_pass = self.UTILS.get_os_variable("FB_PASSWORD", "Password to connect you to facebook.")
        self.facebook.login(fb_user, fb_pass)
        
        #
        # Import facebook contacts.
        #
        friend_count = self.facebook.importAll()

        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Contacts.social_network_contacts"))
        self.UTILS.TEST(len(x) == friend_count, 
                        str(friend_count) + " social network friends listed (there were " + str(len(x)) + ").")
        
        self.contacts.tapSettingsButton()
                
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.totals"))
        y = str(friend_count) + "/" + str(friend_count) + " friends imported"
        self.UTILS.TEST(x.text == y, "After import, import details = '" + y + "' (it was '" + x.text + "').")
        
        