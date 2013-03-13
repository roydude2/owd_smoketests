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
from apps.app_settings import *
from tests.mock_data.contacts import MockContacts

class test_40(GaiaTestCase):
    _Description = "Importing facebook contacts."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 40)
        self.contacts   = AppContacts(self)
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
        self.settings.turn_dataConn_on(False)
        
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
        # Tap the settings button.
        #
        self.contacts.tapSettingsButton()
        
        #
        # Check the message regarding how many fb friends are
        # currently imported (should be none).
        #
        # Something in the way gaiatest removes the contacts when it's initliazed,
        # leaves this message at "x/x contacts imported" if you run this after some 
        # have been added.
        # Therefore ignore this check for now as it'll only be a valid check the very
        # first time you ever run this test, and it only fails because I'm accessing the
        # UI using gaiatest.
        #
        #x = self.UTILS.get_element(*DOM.Facebook.fb_totals)
        #self.UTILS.TEST("No friends imported" in x.text,
            #"Before import, expected 'No friends imported', but instead saw '" + x.text + "'.")
        
        #
        # Import facebook contacts.
        #
        friend_count = self.contacts.fb_importAll()

        #
        # Verify that the contacts were added, by going back to the settings page
        # and checking the totals.
        #
        import time
        time.sleep(2)
        
        #
        # Kill the contacts app and re-launch it, so the imported contacts show up.
        #
        self.apps.kill_all()
        self.contacts.launch()
        
        time.sleep(2)
        
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Contacts.view_all_fb_contacts"))
        self.UTILS.TEST(len(x) == friend_count, "Expected " + str(friend_count) + ", but found " + str(len(x)) + ".")
        
        self.contacts.tapSettingsButton()
                
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.fb_totals"))
        y = str(friend_count) + "/" + str(friend_count) + " friends imported"
        self.UTILS.TEST(x.text == y, "After import, expected '" + y + "', but instead saw '" + x.text + "'.")
        
        