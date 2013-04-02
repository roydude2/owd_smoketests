#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from utils      import UTILS
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_contacts import *

class test_99(GaiaTestCase):
    _Description = "Create a contact via the contacts app."
 
    def setUp(self):
            
        #
        # Set up child objects...
        #
        # Standard.
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        
        # Specific for this test.
        self.contacts   = AppContacts(self)
        
        #
        # Set the timeout for element searches.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Do the tests ...
        #
        
