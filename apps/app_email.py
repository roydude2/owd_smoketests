import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppEmail(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS
            

    def launch(self):
        # For some reason this was causing a marionette error (just in this module).
#        self.apps.kill_all()
        self.app = self.apps.launch('Email')
        self.UTILS.waitForNotDisplayed(20, "Loading overlay stops being displayed", False, DOM.GLOBAL.loading_overlay);
        
    def waitForDone(self):
        #
        # Wait until any progress icon goes away.
        #
#        self.wait_for_element_not_displayed('tag name', 'progress')
        self.UTILS.waitForNotDisplayed(20, "progress icon stops being displayed", False, ('tag name', 'progress'));
        time.sleep(2) # (just to be sure!)

    def goto_folder_from_list(self, p_name):
        #
        # Goto a specific folder in the folder list screen.
        #
        x = self.UTILS.get_element('xpath', DOM.Email.folderList_name_xpath % p_name)
        self.marionette.tap(x)
        
    
    def switchAccount(self, p_address):
        #
        # Add a new account.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_menu_btn"))
        self.marionette.tap(x)
        
        #
        # Are we already in this account?
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.GLOBAL.app_head"))
        self.UTILS.TEST(x, "Current account name is found in the screen header.", True)
        if x.text == p_address:
            # Already here - just go to the Inbox.
            self.goto_folder_from_list("Inbox")
            return True
        
        #
        # We're not in this account already, so let's look for it.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.goto_accounts_btn"))
        self.marionette.tap(x)
        
        x = ('xpath', DOM.GLOBAL.app_head_specific % "Accounts")
        self.UTILS.waitForDisplayed(20, "Accounts header appears.", False, x)
        
        #
        # Check if it's already set up.
        #
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Email.accounts_list_names"))
        for i in x:
            if i.text != "":
                if i.text == p_address:
                    self.marionette.tap(i)
                    
                    self.goto_folder_from_list("Inbox")
                    return True
        
        #
        # It's not setup yet, so we couldn't switch.
        #
        return False


    def remove_accounts_and_restart(self):
        #
        # Remove current email accounts and restart the application.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_menu_btn"))
        self.marionette.tap(x)
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_set_btn"))
        self.marionette.tap(x)
        
        x=('xpath', DOM.GLOBAL.app_head_specific % "Mail settings")
        self.UTILS.waitForDisplayed(20, "Mail settings header appears.", False, x)
        
        #
        # Remove each email address listed ...
        #
        x = self.UTILS.get_elements('class name', 'tng-account-item-label list-text')
        for i in x:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.logComment("i: " + i.text)
                self.marionette.tap(i)
                
                x = ('xpath', DOM.GLOBAL.app_head_specific % i.text)
                self.UTILS.waitForDisplayed(20, i.text + " header appears.", False, x)
                
                # Delete.
                delacc = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_del_acc_btn"))
                self.marionette.tap(delacc)
                
                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_del_conf_btn"))
                self.marionette.tap(delconf)
                
                # Wait for .... something ...??
        
        #
        # Now relaunch the app.
        #
        self.launch()
    
    def setupAccount(self, p_user, p_email, p_pass):
        #
        # Set up a new email account in the email app and login.
        #

        #
        # If we've just started out, email will open directly to "New Account").
        #
        x = self.marionette.find_element(*self.UTILS.verify("DOM.GLOBAL.app_head"))
        if x.text != "New Account":
            #
            # We have at least one emali account setup,
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(p_email):
                return
        
            #
            # It's not setup already, so prepare to set it up!
            #
            x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_set_btn"))
            self.marionette.tap(x)
            
            x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_add_account_btn"))
            self.marionette.tap(x)

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        u = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.username"))
        e = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.email_addr"))
        p = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.password"))

        if p_user != "":
            u.send_keys(p_user)
        if p_email != "":
            e.send_keys(p_email)
        if p_pass != "":
            p.send_keys(p_pass)
            
        btn = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.login_next_btn"))
        self.marionette.tap(btn)
        
        self.UTILS.waitForDisplayed(20, "Email header appears.", False, self.UTILS.verify("DOM.Email.sup_header"))
        
        #
        # Click the 'continue ...' button.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.sup_continue_btn"))
        self.marionette.tap(x)
        
        self.waitForDone()
        
    
    def send_new_email(self, p_target, p_subject, p_message):
        #
        # Compose and send a new email.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.compose_msg_btn"))
        self.marionette.tap(x)
        
        #
        # Wait for 'compose message' header.
        #
        try:
            x = self.UTILS.get_element('xpath', DOM.GLOBAL.app_head_specific % "Compose message")
        except:
            self.UTILS.logResult(False, 
                                 "Taken to 'compose' screen after clicking to compose a new email.")
            self.UTILS.quitTest()
        
        #
        # Put items in the corresponsing fields.
        #
        msg_to      = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.compose_to"))
        msg_subject = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.compose_subject"))
        msg_msg     = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.compose_msg"))
        
        msg_to.send_keys(p_target)
        msg_subject.send_keys(p_subject)
        msg_msg.send_keys(p_message)
        
        #
        # Send the message.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.compose_send_btn"))
        self.marionette.tap(x)
        
        self.waitForDone()
            
        #TEST compose_send_failed_msg - don't know how to swich to this frame!

        #
        # Wait for inbox to re-appear.
        #
        try:
            x = ('xpath', DOM.GLOBAL.app_head_specific % "Inbox")
            self.UTILS.waitForDisplayed(20, "Inbox header appears.", False, x)
        except:
            #
            # Did the email fail to send?
            #
            self.marionette.switch_to_frame()
            x = self.marionette.find_element("xpath","//*[text()='Sending email failed']")
            if x.is_displayed():
                self.UTILS.logResult(False, "Send email succeeded.")
            else:
                #
                # Doesn't look like it, but for some reason we're not back at the Inbox.
                #
                self.UTILS.logResult(False, "Inbox appears after sending an email.")
                
            self.UTILS.quitTest()
        
    def openMailFolder(self, p_folderName):
        #
        # Open a specific mail folder (must be called from "Inbox").
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Email.settings_menu_btn"))
        if not x: self.UTILS.quitTest()
        
        self.marionette.tap(x)
        
        #
        # When we're looking at the folders screen ...
        #
        self.UTILS.waitForDisplayed(20, "Folder list header appears.", False, self.UTILS.verify("DOM.Email.folderList_header"))

        #
        # ... click on the folder were after.
        #
        self.goto_folder_from_list(p_folderName)
        
        #
        # Wait a while for everything to finish populating.
        #
        time.sleep(5)
            
        
    def openMsg(self, p_subject):
        #
        # Assumes we are in the required folder.
        #

        myEmail = self.emailIsInFolder(p_subject)
        if myEmail:
            #
            # We found it - open the email.
            #
            myEmail.click()
            return True
            
        else:
            self.UTILS.logResult(False, "Able to find and open the message with subject '"  + p_subject + "' in this folder.")
            return False

    
    def emailIsInFolder(self, p_subject):
        #
        # Verify an email is in this folder with the expected subject.
        #

        #
        # Because this can take a while, try to "wait_for_element..." 10 times.
        #
        loops = 15
        while loops >= 0:
            try:
                #
                # This DOM element might not exist in the screen yet, so don't
                # 'verify' it!
                #
                self.wait_for_element_displayed(*DOM.Email.folder_subject_list)
                
                #
                # *something* is now in the folder ...
                #
                z = self.UTILS.get_elements(*self.UTILS.verify("DOM.Email.folder_subject_list"))
                for i in z:
                    #
                    # Do any of the folder items match our subject?
                    #
                    if i.text == p_subject:
                        return i
            except:
                #
                # Nothing is in the folder yet, just ignore and loop again.
                #
                pass
            
            #
            # Either the folder is still empty, or none of the items in it match our
            # subject yet.
            # Wait a couple fo seconds and try again.
            # 
            x = self.marionette.find_element(*self.UTILS.verify("DOM.Email.folder_refresh_button"))
            self.marionette.tap(x)
            
            time.sleep(5)
            loops = loops - 1
        
        return False
