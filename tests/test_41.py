#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests.mock_data.contacts import MockContacts
import time

class test_41(GaiaTestCase):
    _Description = "Link a facebook contact."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
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
        self.contacts.viewContact(self.Contact_1['name'])
        
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
        self.UTILS.TEST(self.UTILS.headerCheck(self.Contact_1['name']), "Header is '"+ self.Contact_1['name'] +"'.")

        #
        # Verify that we're now linked.
        #
        self.contacts.verifyLinked(self.Contact_1['name'], fb_email)