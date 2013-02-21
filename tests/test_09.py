import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_contacts, app_messages
from tests.mock_data.contacts import MockContacts
from gaiatest import GaiaTestCase

class test_9(GaiaTestCase):
    _Description = "Send an SMS to a contact from the contacts app."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 8)
        self.contacts   = app_contacts.main(self, self.testUtils)
        self.messages   = app_messages.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)

        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Roy

        #
        # Establish which phone number to use.
        #
        import os
        self.contact_1["tel"]["value"] = os.environ['TEST_SMS_NUM']
        self.testUtils.reportComment("Sending sms to telephone number: " + self.contact_1["tel"]["value"])
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)
            
    def tearDown(self):
        self.testUtils.reportResults()
        
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
        self.wait_for_element_displayed(*DOM.Contacts.sms_button)
        smsBTN = self.testUtils.get_element(*DOM.Contacts.sms_button)
        self.testUtils.clickNTap(smsBTN)

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        self.testUtils.switchFrame(*DOM.Messages.frame_locator)
        #self.testUtils.connect_to_iframe(DOM.Messages.iframe_location)

        #
        # TEST: correct name is in the header of this sms.
        #
        headerName = self.testUtils.get_element('xpath', DOM.GLOBAL.app_head % self.contact_1['name'])
        self.testUtils.TEST(headerName.is_displayed(), "Contact name not in 'Send message' header")

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg("Smoke test 9 sms - please reply with the word 'ok'.")
        
        #
        # Click send.
        #
        self.messages.sendSMS()
       
        #
        # There's a bug in gaia at the moment - if you switch around too quickly the 'new sms' notifier
        # can get stuck at the top of the screen for a looooong time.
        # To make sure we don't cause that, wait a while before trying to display the status bar.
        #
        import time
        time.sleep(10)
        
        #
        # Wait for return message (to confirm communication).
        #
        self.messages.waitForNewSMS()

        #
        # Read the new message.
        #
        returnedSMS = self.messages.readNewSMS()
        
        #
        # TEST: The returned message is as expected.
        #
        self.testUtils.TEST((returnedSMS.lower() == "ok"), 
            "Expected text to be 'ok' but was '" + returnedSMS + "'")

        #
        # Because of a bug, the message notifier remains in the header until you restart the
        # messaging app, so restart it just to remove the notification.
        #
        self.testUtils.goHome()
        self.messages.launch()
