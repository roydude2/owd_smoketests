import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_contacts
from smoketests.mocks.mock_contact import MockContact
from gaiatest import GaiaTestCase

class test_7(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = RoyUtils.testUtils(self, 7)
        self.contacts   = app_contacts.main(self, self.testUtils)
        
        # Set the timeout for element searches.
        self.marionette.set_search_timeout(50)

        # Get details of our test contact.
        self.Contact_1 = MockContact().Contact_1
        
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
        # Create new contact.
        #
        self.contacts.createNewContact(self.Contact_1)
        
        #
        # TEST: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.checkViewContactDetails(self.Contact_1)
