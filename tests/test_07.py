#
# Imports which are standard for all test cases.
#
# RoyNEW
# Royanothernew
# ROYROYROY
# ROy what happens now??
# Another roy
import sys
sys.path.insert(1, "./")

from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests.mock_data.contacts import MockContacts

class test_7(GaiaTestCase):
    _Description = "Create a contact via the contacts app."
 
    def setUp(self):
            
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
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
        
        #
        # Store our picture on the device.
        #
        self.UTILS.addFileToDevice('./tests/resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Create our contact.
        #
        self.contacts.createNewContact(self.Contact_1,"gallery")
        
        #
        # Verify our contact.
        #
        self.contacts.verifyImageInAllContacts(self.Contact_1['name'])
        self.contacts.checkViewContactDetails(self.Contact_1, True)
