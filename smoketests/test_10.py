import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_messages
from smoketests.mocks.mock_contact import MockContact
from gaiatest import GaiaTestCase

class test_10(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils  = RoyUtils.testUtils(self, 8)
        self.messages   = app_messages.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
        
        # Change the settings to vibration only.
        self.data_layer.set_setting("vibration.enabled", True)
        self.data_layer.set_setting("audio.volume.notification", 0)
        
        # Establish which phone number to use.
        import os
        self.target_telNum = os.environ['TEST_10_NUM']
        
        #print " "
        #print " "
        #ans = raw_input("Enter mobile number of the phone being tested (sending a message to itself for now): ")
        #if ans != "":
            #self.Roy["tel"]["value"] = ans
        
        self.testUtils.reportComment("Sending sms to telephone number: " + self.target_telNum)
        
        
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
        
        # Cannot get this to work (pull down the notification bar WAS working ... but now it's not! ;( )
        ##
        ## Go to the home screen and wait for new message notification in home screen.
        ##
        ##x = self.messages.openNewSMS_homescreen()
        ##self.testUtils.testTrue(x, "Could not load new message from notification in the home screen, aborting test!")
        ##if not x:
            ##return 1 # Cannot continue with this test.
            
        #self.testUtils.goHome()
        #self.testUtils.displayStatusBar()
        #self.testUtils.waitForStatusBarNew()
        #self.testUtils.openStatusBarNewNotif(DOMS.Messages.statusbar_new_sms_url)
        #self.testUtils.connect_to_iframe("app://sms.gaiamobile.org/index.html")
        ##self.testUtils.switchFrame(*DOMS.Messages.frame_locator)
        
        #
        # Wait for (because I can't watch from the home screen as planned!), then read the new message.
        #
        self.messages.waitForNewSMS()
        returnedSMS = self.messages.readNewSMS()
        
        #
        # TEST: The returned message is as expected.
        #
        self.testUtils.testTrue((returnedSMS.lower() == "ok"), 
            "Expected text to be 'ok' but was '" + returnedSMS + "'")
