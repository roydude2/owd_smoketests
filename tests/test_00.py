import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_contacts
from tests.mock_data.contacts import MockContacts
from gaiatest import GaiaTestCase

class test_40(GaiaTestCase):
    _Description = "Importing facebook contacts."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 40)
        self.contacts   = app_contacts.main(self, self.UTILS)
                
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
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Select my contact.
        #
        self.contacts.viewContact(self.Contact_1)
        
        #
        # Tap link button to go to facebook.
        #
        self.contacts.tapLinkButton()
        
        import time
        #time.sleep(4)
        #self.UTILS.connect_to_iframe_by_id("fb-curtain")
        time.sleep(2)
        self.UTILS.savePageHTML("/tmp/roy1.html")
