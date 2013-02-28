import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_contacts
from tests.mock_data.contacts import MockContacts
from gaiatest import GaiaTestCase

class test_8(GaiaTestCase):
    _Description = "Edit a contact in the contacts app."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 8)
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
        self.Contact_2 = MockContacts().Contact_2

        #
        # We're not testing adding a contact, so just stick one 
        # into the database.
        #
        self.data_layer.insert_contact(self.Contact_1)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Edit the contact with the new details.
        #
        self.contacts.editContact(self.Contact_1, self.Contact_2)
        
        #
        # TEST: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.checkViewContactDetails(self.Contact_2)         
        
        #
        # TEST: The 'edit contact' page shows the correct details for this new contact.
        #
        self.contacts.checkEditContactDetails(self.Contact_2) 

  
        
