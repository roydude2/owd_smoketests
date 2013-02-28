#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_email
from gaiatest import GaiaTestCase
import time

#
# As I can't see ANY different between read and unread emails in the html,
# I need to rely on a totally unique subject line to identify the precise
# message sent between the two test accounts.
# Because of this I need to stay in the same python instance to remember
# the subject line I generated (and guarantee 100% that 22 ran before 23).
#
class test_22(GaiaTestCase):
    _Description = "Combination of 22 and 23 Send and receive an email between hotmail accounts (will pause for 60s between tests)."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 22)
        self.Email      = app_email.main(self, self.UTILS)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Establish parameters.
        #
        self.subject = "Test 22 - " + str(time.time())
        self.body    = "This is the test email body."
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
        self.UTILS.reportComment("Using subject    '" + self.subject + "'")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        ##################################################
        #
        # Smoketest 22
        
        #
        # Launch Email app.
        #
        self.Email.launch()
        
        #
        # Login.
        #
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
        
        #
        # Count the messages in the sent mail folder.
        #
        sent_emails_before = self.Email.countMessagesInFolder("Sent")
        
        #
        # Return to the Inbox.
        #
        self.Email.openMailFolder("Inbox")
        
        #
        # At the inbox, compose a new email.
        #
        self.Email.send_new_email(self.EMAIL2, self.subject, self.body)

        #
        # Report on how many items were in the Sent folder.
        #
        sent_emails_after = self.Email.countMessagesInFolder("Sent")
        total_sent = sent_emails_after - sent_emails_before
        self.UTILS.TEST(total_sent == 1,
            "Expected 1 more 'Sent' email, but found " + str(total_sent) + ".")
        
        #
        # Check our email is in the sent folder.
        #
        time.sleep(20)
        self.Email.openMailFolder("Sent")
        self.UTILS.TEST(self.Email.emailIsInFolder(self.subject),
            "Email was not found in the Sent folder after being sent.")
        

        #
        # Give the email time to arrive.
        #
        time.sleep(60)

        ##################################################
        #
        # Smoketest 23
        
        #
        # Launch Email app.
        #
        self.Email.launch()
        
        #
        # Login.
        #
        self.Email.setupAccount(self.USER2, self.EMAIL2, self.PASS2)
            
        #
        # Open the email.
        #
        self.UTILS.TEST(self.Email.openUnreadMsg(self.subject),
            "Unable to find an email with the subject '" + self.subject)
            
        #
        # Verify the contents.
        #
        x = self.UTILS.get_element(*DOM.Email.open_email_from)
        self.UTILS.TEST(x.text == self.EMAIL1, 
            "Expected 'From' field to be '" + self.EMAIL1 + "', but it was '" + x.text + "'.")

        x = self.UTILS.get_element(*DOM.Email.open_email_to)
        self.UTILS.TEST(x.text == self.EMAIL2, 
            "Expected 'To' field to be '" + self.EMAIL2 + "', but it was '" + x.text + "'.")

        x = self.UTILS.get_element(*DOM.Email.open_email_subject)
        self.UTILS.TEST(x.text == self.subject, 
            "Expected 'From' field to be '" + self.subject + "', but it was '" + x.text + "'.")
        
