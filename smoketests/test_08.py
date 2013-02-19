import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_contacts
from smoketests.mocks.mock_contact import MockContact
from gaiatest import GaiaTestCase

class test_8(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils  = RoyUtils.testUtils(self, 8)
        self.contacts   = app_contacts.main(self, self.testUtils)
                
        # Set timeout for element searches.
        self.marionette.set_search_timeout(50)

        # Get details of our test contacts.
        self.Contact_1 = MockContact().Contact_1
        self.Contact_2 = MockContact().Contact_2

        # We're not testing adding a contact, so just stick one 
        # into the database.
        self.data_layer.insert_contact(self.Contact_1)
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
        
    def tearDown(self):
        self.testUtils.reportResults()
        
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

  
        
