#
# Runs through composing and sending an email as one user, then
# receiving it as another user.
#
# As I can't see ANY different between read and unread emails in the html,
# I need to rely on a totally unique subject line to identify the precise
# message sent between the two test accounts.
# Because of this I need to stay in the same python instance to remember
# the subject line I generated (and guarantee 100% that 24 ran before 25).
#
# Currently used by tests 22, 23, 24 and 25 (combined to 22 and 24).
#

#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from marionette import Marionette
from tools      import TestUtils
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_settings import *
from apps.app_email import *
import os, time

class main():
    
    def __init__(self, 
                 p_parent, 
                 p_testNum, 
                 p_sentFolderName,
                 p_email1,
                 p_user1,
                 p_pass1,
                 p_email2,
                 p_user2,
                 p_pass2):
                     
        #
        # Establish parameters.
        #
        self.body           = "This is the test email body."
        self.USER1          = p_user1
        self.EMAIL1         = p_email1
        self.PASS1          = p_pass1
        self.USER2          = p_user2
        self.EMAIL2         = p_email2
        self.PASS2          = p_pass2
        self.apps           = p_parent.apps
        self.sentFolderName = p_sentFolderName
        self.Email          = AppEmail(p_parent)
        self.settings       = AppSettings(p_parent)
        self.subject        = "Test " + p_testNum + " - " + str(time.time())
        
                # Just so I get 'autocomplete' in my IDE!
        self.marionette     = Marionette()
        self.UTILS          = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS

        self.UTILS.logComment("Using subject \"" + self.subject + "\".")
        
        self.marionette.set_search_timeout(50)
        p_parent.lockscreen.unlock()
        
        #
        # Make sure we have some data connectivity.
        #
        p_parent.data_layer.enable_wifi()
        self.settings.turn_dataConn_on_if_required()
        
    def run(self):

        ##################################################
        #
        # SEND EMAIL
        
        #
        # Launch Email app.
        #
        self.Email.launch()
        
        #
        # Login.
        #
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
        
        #
        # Return to the Inbox.
        #
        self.Email.openMailFolder("Inbox")
        
        #
        # At the inbox, compose a new email.
        #
        self.Email.send_new_email(self.EMAIL2, self.subject, self.body)

        #
        # Check our email is in the sent folder.
        #
        self.Email.openMailFolder(self.sentFolderName)
        time.sleep(10)
        self.UTILS.TEST(self.Email.emailIsInFolder(self.subject),
            "Email is found in the Sent folder after being sent.")
        
        #
        # Give the email time to arrive.
        #
#        time.sleep(180)

        ##################################################
        #
        # RECEIVE EMAIL
        
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
        self.UTILS.TEST(self.Email.openMsg(self.subject),
            "Found an email with the subject '" + self.subject + "'", True)
        
        #
        # Verify the contents.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.open_email_from"))
        self.UTILS.TEST(x.text == self.EMAIL1, 
            "'From' field = '" + self.EMAIL1 + "' (it was '" + x.text + "').")

        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.open_email_to"))
        self.UTILS.TEST(x.text == self.EMAIL2, 
            "'To' field = '" + self.EMAIL2 + "', (it was '" + x.text + "').")

        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.open_email_subject"))
        self.UTILS.TEST(x.text == self.subject, 
            "'From' field = '" + self.subject + "', (it was '" + x.text + "').")
        

