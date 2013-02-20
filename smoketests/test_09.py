import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_contacts, app_messages
from smoketests.mocks.mock_contact import MockContact
from gaiatest import GaiaTestCase, GaiaApps

class test_9(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils  = RoyUtils.testUtils(self, 8)
        self.contacts   = app_contacts.main(self, self.testUtils)
        self.messages   = app_messages.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)

        # Prepare the contact we're going to insert.
        self.contact_1 = MockContact().Roy

        # Establish which phone number to use.
        import os
        self.contact_1["tel"]["value"] = os.environ['TEST_10_NUM']
        
        #print " "
        #print " "
        #ans = raw_input("Enter mobile number of the phone being tested (sending a message to itself for now): ")
        #if ans != "":
            #self.contact_1["tel"]["value"] = ans
        
        self.testUtils.reportComment("Sending sms to telephone number: " + self.contact_1["tel"]["value"])
        
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        self.data_layer.insert_contact(self.contact_1)
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
    
        # Launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*DOMS.GLOBAL.loading_overlay)
        
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
        
        # Tap the sms button in the view details screen to go to the sms page.
        self.wait_for_element_displayed(*DOMS.Contacts.sms_button)
        smsBTN = self.testUtils.get_element(*DOMS.Contacts.sms_button)
        self.testUtils.clickNTap(smsBTN)

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        self.testUtils.switchFrame(*DOMS.Messages.frame_locator)
        #self.testUtils.connect_to_iframe(DOMS.Messages.iframe_location)

        #
        # TEST: correct name is in the header of this sms.
        #
        headerName = self.testUtils.get_element('xpath', DOMS.GLOBAL.app_head % self.contact_1['name'])
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
