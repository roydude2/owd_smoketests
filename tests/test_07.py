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
from tests.mock_data.contacts import MockContacts

class test_7(GaiaTestCase):
    _Description = "Create a contact via the contacts app."
 
    def setUp(self):
            
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 7)
        self.contacts   = AppContacts(self)
        
        #
        # Set the timeout for element searches.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()

        #
        # Get details of our test contact.
        #
        self.Contact_1 = MockContacts().Contact_1
        
        
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
        # TEST: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.checkViewContactDetails(self.Contact_1)
