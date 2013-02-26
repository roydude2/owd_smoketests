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
# the subject line I generated (and guarantee 100% that 24 ran before 25).
#
class test_22(GaiaTestCase):
    _Description = "Combination of 24 and 25 Send and receive an email between gmail accounts (will pause for 30s between tests)."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, 24)
        self.Email      = app_email.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Establish parameters.
        #
        self.subject = "Test 24 - " + str(time.time())
        self.body    = "This is the test email body."
        self.USER1  = self.testUtils.get_os_variable("GMAIL_1_USER"  , "Gmail 1 username")
        self.EMAIL1 = self.testUtils.get_os_variable("GMAIL_1_EMAIL" , "Gmail 1 email")
        self.PASS1  = self.testUtils.get_os_variable("GMAIL_1_PASS"  , "Gmail 1 password")
        self.USER2  = self.testUtils.get_os_variable("GMAIL_2_USER"  , "Gmail 2 username")
        self.EMAIL2 = self.testUtils.get_os_variable("GMAIL_2_EMAIL" , "Gmail 2 email")
        self.PASS2  = self.testUtils.get_os_variable("GMAIL_2_PASS"  , "Gmail 2 password")
        self.testUtils.reportComment("Using username 1 '" + self.USER1 + "'")
        self.testUtils.reportComment("Using password 1 '" + self.PASS1 + "'")
        self.testUtils.reportComment("Using email    1 '" + self.EMAIL1 + "'")
        self.testUtils.reportComment("Using username 2 '" + self.USER2 + "'")
        self.testUtils.reportComment("Using password 2 '" + self.PASS2 + "'")
        self.testUtils.reportComment("Using email    2 '" + self.EMAIL2 + "'")
        self.testUtils.reportComment("Using subject    '" + self.subject + "'")
        
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        ##################################################
        #
        # Smoketest 24
        
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
        sent_emails_before = self.Email.countMessagesInFolder("Sent Mail")
        
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
        sent_emails_after = self.Email.countMessagesInFolder("Sent Mail")
        self.testUtils.reportComment(
            "Sent folder count before sending: " + str(sent_emails_before) + ", and after: " + str(sent_emails_after))

        total_sent = sent_emails_after - sent_emails_before
        self.testUtils.TEST(total_sent == 1,
            "Expected 1 more 'Sent' email, but found " + str(total_sent) + ".")
        
        #
        # Check our email is in the sent folder.
        #
        self.Email.openMailFolder("Sent Mail")
        self.testUtils.TEST(self.Email.emailIsInFolder(self.subject),
            "Email was not found in the Sent Mail folder after being sent.")
        


        #
        # Give the email time to arrive ....
        #
        time.sleep(30)

        ##################################################
        #
        # Smoketest 25
        
        #
        # Launch Email app.
        #
        self.Email.launch()
        
        #
        # Login.
        #
        self.Email.setupAccount(self.USER2, self.EMAIL2, self.PASS2)
            
        #
        # Open the email, matching the subject.
        #
        self.testUtils.TEST(self.Email.openUnreadMsg(self.subject),
            "Unable to find an email with the subject '" + self.subject, True)
            
        #
        # Verify the contents.
        #
        x = self.testUtils.get_element(*DOM.Email.open_email_from)
        self.testUtils.TEST(x.text == self.EMAIL1, 
            "Expected 'From' field to be '" + self.EMAIL1 + "', but it was '" + x.text + "'.")

        x = self.testUtils.get_element(*DOM.Email.open_email_to)
        self.testUtils.TEST(x.text == self.EMAIL2, 
            "Expected 'To' field to be '" + self.EMAIL2 + "', but it was '" + x.text + "'.")

        x = self.testUtils.get_element(*DOM.Email.open_email_subject)
        self.testUtils.TEST(x.text == self.subject, 
            "Expected 'From' field to be '" + self.subject + "', but it was '" + x.text + "'.")
        
