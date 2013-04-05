import DOM, time
from gaiatest   import GaiaTestCase
from utils      import UTILS
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
        self.UTILS      = UTILS(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS
            

    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Email')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");
        
    def waitForDone(self):
        #
        # Wait until any progress icon goes away.
        #
        self.UTILS.waitForNotElements(('tag name', 'progress'), "Progress icon");
        time.sleep(2) # (just to be sure!)

    def goto_folder_from_list(self, p_name):
        #
        # Goto a specific folder in the folder list screen.
        #
        x = self.UTILS.getElement(('xpath', DOM.Email.folderList_name_xpath % p_name), "Link to folder '" + p_name + "'")
        self.marionette.tap(x)
        
    
    def switchAccount(self, p_address):
        #
        # Add a new account.
        #
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        self.marionette.tap(x)
        
        #
        # Are we already in this account?
        #
        x = self.UTILS.getElement(DOM.GLOBAL.app_head, "Header")
        if x.text == p_address:
            # Already here - just go to the Inbox.
            self.goto_folder_from_list("Inbox")
            return True
        
        #
        # We're not in this account already, so let's look for it.
        #
        x = self.UTILS.getElement(DOM.Email.goto_accounts_btn, "Accounts button")
        self.marionette.tap(x)
        
        x = ('xpath', DOM.GLOBAL.app_head_specific % "Accounts")
        self.UTILS.waitForElements(x, "Accounts header", True, 20, False)
        
        #
        # Check if it's already set up (this may be empty, so don't test for this element).
        #
        x = self.marionette.find_elements(*DOM.Email.accounts_list_names)
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
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings button")
        self.marionette.tap(x)
        
        x = self.UTILS.getElement(DOM.Email.settings_set_btn, "Set settings button")
        self.marionette.tap(x)
        
        x=('xpath', DOM.GLOBAL.app_head_specific % "Mail settings")
        self.UTILS.waitForElements(x, "Mail settings", True, 20, False)
        
        #
        # Remove each email address listed ...
        #
        x = self.UTILS.getElements(DOM.Email.email_accounts_list,
                                   "Email accounts list", False, 20, False)
        for i in x:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.logComment("i: " + i.text)
                self.marionette.tap(i)
                
                x = ('xpath', DOM.GLOBAL.app_head_specific % i.text)
                self.UTILS.waitForElements(x, i.text + " header", True, 20, False)
                
                # Delete.
                delacc = self.UTILS.getElement(DOM.Email.settings_del_acc_btn, "Delete account button")
                self.marionette.tap(delacc)
                
                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.getElement(DOM.Email.settings_del_conf_btn, "Confirm delete button")
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
        x = self.UTILS.getElement(DOM.GLOBAL.app_head, "Application header")
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
            x = self.UTILS.getElement(DOM.Email.settings_set_btn, "Settings set button")
            self.marionette.tap(x)
            
            x = self.UTILS.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            self.marionette.tap(x)

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        u = self.UTILS.getElement(DOM.Email.username, "Username field")
        e = self.UTILS.getElement(DOM.Email.email_addr, "Email address field")
        p = self.UTILS.getElement(DOM.Email.password, "Password field")

        if p_user != "":
            u.send_keys(p_user)
        if p_email != "":
            e.send_keys(p_email)
        if p_pass != "":
            p.send_keys(p_pass)
            
        btn = self.UTILS.getElement(DOM.Email.login_next_btn, "Login - 'next' button")
        self.marionette.tap(btn)
        
        self.UTILS.waitForElements(DOM.Email.sup_header, "Email header", True, 20, False)
        
        #
        # Click the 'continue ...' button.
        #
        x = self.UTILS.getElement(DOM.Email.sup_continue_btn, "Continue button")
        self.marionette.tap(x)
        
        self.waitForDone()
        
    
    def send_new_email(self, p_target, p_subject, p_message):
        #
        # Compose and send a new email.
        #
        x = self.UTILS.getElement(DOM.Email.compose_msg_btn, "Compose message button")
        self.marionette.tap(x)
        
        #
        # Wait for 'compose message' header.
        #
        x = self.UTILS.getElement(('xpath', DOM.GLOBAL.app_head_specific % "Compose message"),
                                  "Compose message header")
        
        #
        # Put items in the corresponsing fields.
        #
        msg_to      = self.UTILS.getElement(DOM.Email.compose_to, "'To' field")
        msg_subject = self.UTILS.getElement(DOM.Email.compose_subject, "'Subject' field")
        msg_msg     = self.UTILS.getElement(DOM.Email.compose_msg, "Message field")
        
        msg_to.send_keys(p_target)
        msg_subject.send_keys(p_subject)
        msg_msg.send_keys(p_message)
        
        #
        # Send the message.
        #
        x = self.UTILS.getElement(DOM.Email.compose_send_btn, "Send button")
        self.marionette.tap(x)
        
        self.waitForDone()
            
        #TEST compose_send_failed_msg - don't know how to swich to this frame!

        #
        # Wait for inbox to re-appear.
        #
        x = ('xpath', DOM.GLOBAL.app_head_specific % "Inbox")
        y = self.UTILS.waitForElements(x, "Inbox")
        
    def openMailFolder(self, p_folderName):
        #
        # Open a specific mail folder (must be called from "Inbox").
        #
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings menu button")        
        self.marionette.tap(x)
        
        #
        # When we're looking at the folders screen ...
        #
        self.UTILS.waitForElements(DOM.Email.folderList_header, "Folder list header appears.", True, 20, False)

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
        self.UTILS.TEST(myEmail, "Found email with subject '" + p_subject + "'.")
        if myEmail:
            #
            # We found it - open the email.
            #
            myEmail.click()
            
            #
            # Check it opened.
            #
            boolOK = True
            try:
                self.wait_for_element_displayed(*DOM.Email.open_email_from)
                return True
            except:
                return False
            
        else:
            return False

    
    def emailIsInFolder(self, p_subject):
        #
        # Verify an email is in this folder with the expected subject.
        #

        #
        # Because this can take a while, try to "wait_for_element..." several times.
        #
        loops = 15
        while loops > 0:
            try:
                #
                # Look through any entries found in the folder ...
                #
                z = self.UTILS.getElements(DOM.Email.folder_subject_list, "Folder item list")
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
            # Wait a couple for seconds and try again.
            # 
            x = self.UTILS.getElement(DOM.Email.folder_refresh_button, "Refresh button")
            self.marionette.tap(x)
            
            time.sleep(5)
            loops = loops - 1
        
        return False
