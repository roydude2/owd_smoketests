import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_messages
from gaiatest import GaiaTestCase

class test_10(GaiaTestCase):
    _Description = "Send and receive an SMS via the messaging app."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 8)
        self.messages   = app_messages.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        
        #
        # Change the settings to vibration only (backdoor method since
        # this isn't what we're testing).
        #
        self.data_layer.set_setting("vibration.enabled", True)
        self.data_layer.set_setting("audio.volume.notification", 0)
        
        #
        # Establish which phone number to use.
        #
        import os
        self.target_telNum = os.environ['TEST_SMS_NUM']
        self.testUtils.reportComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS(self.target_telNum, "Smoke test 10 sms - please reply with the word 'ok'.")
        
        #
        # Go home and wait for the notification.
        #
        self.testUtils.goHome()
        
        #
        # There's a bug in gaia at the moment - if you switch around too quickly the 'new sms' notifier
        # can get stuck at the top of the screen for a looooong time.
        # To make sure we don't cause that, wait a while before trying to display the status bar.
        #
        import time
        time.sleep(10)
        
        #
        # Wait for the notification to appear in the utility / noification / status bar (has too many names!).
        # Then open the bar.
        # Then click on the new message notification.
        #
        self.testUtils.waitForStatusBarNew()
        self.testUtils.displayStatusBar()
        self.testUtils.openStatusBarNewNotif(DOM.Messages.statusbar_new_sms_url)

        #
        # Switch focus to the sms app and read the latest message.
        #
        self.testUtils.connect_to_iframe(DOM.Messages.iframe_location)
        returnedSMS = self.messages.readLastSMSInThread()
        
        #
        # TEST: The returned message is as expected.
        #
        self.testUtils.TEST((returnedSMS.lower() == "ok"), 
            "Expected text to be 'ok' but was '" + returnedSMS + "'")
