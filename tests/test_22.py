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
from tests.shared_test_functions import EMAIL_SEND_AND_RECEIVE

class test_22_23(GaiaTestCase):
    _Description = "Combination of 22 and 23 Send and receive an email between hotmail accounts (very long pauses between tests)."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 24)
        
        #
        # Establish parameters.
        #
        self.USER1  = self.UTILS.get_os_variable("HOTMAIL_1_USER"  , "Hotmail 1 username")
        self.EMAIL1 = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL" , "Hotmail 1 email")
        self.PASS1  = self.UTILS.get_os_variable("HOTMAIL_1_PASS"  , "Hotmail 1 password")
        self.USER2  = self.UTILS.get_os_variable("HOTMAIL_2_USER"  , "Hotmail 2 username")
        self.EMAIL2 = self.UTILS.get_os_variable("HOTMAIL_2_EMAIL" , "Hotmail 2 email")
        self.PASS2  = self.UTILS.get_os_variable("HOTMAIL_2_PASS"  , "Hotmail 2 password")
        self.UTILS.reportComment("Using username 1 '" + self.USER1 + "'")
        self.UTILS.reportComment("Using password 1 '" + self.PASS1 + "'")
        self.UTILS.reportComment("Using email    1 '" + self.EMAIL1 + "'")
        self.UTILS.reportComment("Using username 2 '" + self.USER2 + "'")
        self.UTILS.reportComment("Using password 2 '" + self.PASS2 + "'")
        self.UTILS.reportComment("Using email    2 '" + self.EMAIL2 + "'")
        
        self.EMAIL  = EMAIL_SEND_AND_RECEIVE.main(self, 
                                                  "22 and 23",
                                                  "Sent",
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
