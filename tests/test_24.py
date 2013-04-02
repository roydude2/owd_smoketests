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
from tests.shared_test_functions import EMAIL_SEND_AND_RECEIVE

class test_24_25(GaiaTestCase):
    _Description = "Combination of 24 and 25 - Send and receive an email between gmail accounts."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = UTILS(self)
        
        #
        # Establish parameters.
        #
        self.USER1  = self.UTILS.get_os_variable("GMAIL_1_USER"  , "Gmail 1 username")
        self.EMAIL1 = self.UTILS.get_os_variable("GMAIL_1_EMAIL" , "Gmail 1 email")
        self.PASS1  = self.UTILS.get_os_variable("GMAIL_1_PASS"  , "Gmail 1 password")
        self.USER2  = self.UTILS.get_os_variable("GMAIL_2_USER"  , "Gmail 2 username")
        self.EMAIL2 = self.UTILS.get_os_variable("GMAIL_2_EMAIL" , "Gmail 2 email")
        self.PASS2  = self.UTILS.get_os_variable("GMAIL_2_PASS"  , "Gmail 2 password")
        self.UTILS.logComment("Using username 1 '" + self.USER1 + "'")
        self.UTILS.logComment("Using password 1 '" + self.PASS1 + "'")
        self.UTILS.logComment("Using email    1 '" + self.EMAIL1 + "'")
        self.UTILS.logComment("Using username 2 '" + self.USER2 + "'")
        self.UTILS.logComment("Using password 2 '" + self.PASS2 + "'")
        self.UTILS.logComment("Using email    2 '" + self.EMAIL2 + "'")
        
        self.EMAIL  = EMAIL_SEND_AND_RECEIVE.main(self, 
                                                  "24 and 25",
                                                  "Sent Mail",
                                                  self.EMAIL1,
                                                  self.USER1,
                                                  self.PASS1,
                                                  self.EMAIL2,
                                                  self.USER2,
                                                  self.PASS2)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.EMAIL.run()
