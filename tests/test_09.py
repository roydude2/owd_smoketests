#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

#
# Imports particular to this test case.
#
from tests.mock_data.contacts import MockContacts

class test_9(GaiaTestCase):
    _Description = "Send an SMS to a contact from the contacts app."
    
    _TestMsg     = "Smoke test 9 sms - reply with this same message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = AppContacts(self)
        self.messages   = AppMessages(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()

        self.data_layer.set_setting("vibration.enabled", True)
        self.data_layer.set_setting("audio.volume.notification", 0)

        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Roy

        #
        # Establish which phone number to use.
        #
        self.contact_1["tel"]["value"] = self.UTILS.get_os_variable("TEST_SMS_NUM", "Mobile number for SMS tests (test 9)")
        self.UTILS.logComment("Using target telephone number " + self.contact_1["tel"]["value"])
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)
            
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.contact_1)
        
        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement(DOM.Contacts.sms_button, "Send SMS button")
        self.marionette.tap(smsBTN)

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)

        #
        # TEST: this automatically opens the 'send SMS' screen, so
        # check the correct name is in the header of this sms.
        #
        self.UTILS.TEST(self.UTILS.headerCheck(self.contact_1['name']),
                        "'Send message' header = '" + self.contact_1['name'] + "'.")
    
        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
        
        #
        # There's a bug in gaia at the moment - if you switch around too quickly the 'new sms' notifier
        # can get stuck at the top of the screen 'forever'.
        # To try and avoid that, wait a while before displaying the status bar.
        #
        time.sleep(10)
        
        #
        # Wait 3 mins for return message (to confirm communication) - uses the contacts name if it matches one, not the number.
        #
        x = self.messages.waitForSMSNotifier(self.contact_1["name"], 180)        
        self.UTILS.TEST(x, "Found new msg.", True)
        
        #
        # Switch back to the sms app. (if we managed to click).
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        
        #
        # Read the new message.
        # (For this you need the number).
        #
        returnedSMS = self.messages.readNewSMS(self.contact_1["tel"]["value"])
        
        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        self.UTILS.TEST((returnedSMS.lower() == self._TestMsg.lower()), 
            "SMS text = '" + self._TestMsg + "' (it was '" + returnedSMS + "').")

        #
        # Because of a bug, the message notifier remains in the header until you restart the
        # messaging app, so restart it just to remove the notification.
        #
        self.UTILS.goHome()
        self.messages.launch()
