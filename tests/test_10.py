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
from apps.app_messages import *

class test_10(GaiaTestCase):
    _Description = "Send and receive an SMS via the messaging app."
    
    _TestMsg     = "Smoke test 10 sms - reply with this same message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self)
        self.messages   = AppMessages(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Change the settings to vibration only (backdoor method since
        # this isn't what we're testing).
        #
        self.data_layer.set_setting("vibration.enabled", True)
        self.data_layer.set_setting("audio.volume.notification", 0)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("TEST_SMS_NUM", "Mobile number for SMS tests (test 10)")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS(self.target_telNum, self._TestMsg)
        
        #
        # Go home and wait for the notification.
        #
        self.UTILS.goHome()
        
        #
        # Wait 3 mins for the notification to appear in the utility / noification / status bar (has too many names!).
        # Then open the bar and click on the new message notification.
        #
        x = self.messages.waitForSMSNotifier(self.target_telNum, 180)
        self.UTILS.TEST(x, "Found new msg.", True)
        
        self.messages.clickSMSNotifier(self.target_telNum)

        #
        # Switch focus to the sms app and read the latest message.
        #
        returnedSMS = self.messages.readLastSMSInThread()
        
        #
        # TEST: The returned message is as expected.
        #
        self.UTILS.TEST((returnedSMS.lower() == self._TestMsg.lower()), 
            "SMS text = '" + self._TestMsg + "' (it was '" + returnedSMS + "').")
