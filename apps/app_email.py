from apps import DOM
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.UTILS  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.parent.apps.kill_all()
        self.app = self.parent.apps.launch('Email')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)
        
    #
    # Wait until any progress icon goes away.
    #
    def waitForDone(self):
        self.parent.wait_for_element_not_displayed('tag name', 'progress')
        time.sleep(2) # (just to be sure!)

    #
    # Goto a specific folder in the folder list screen.
    #
    def goto_folder_from_list(self, p_name):
        x = self.UTILS.get_element('xpath', DOM.Email.folderList_name_xpath % p_name)
        self.marionette.tap(x)
        
    
    #
    # Add a new account.
    #
    def switchAccount(self, p_address):
        x = self.UTILS.get_element(*DOM.Email.settings_menu_btn)
        self.marionette.tap(x)
        
        #
        # Are we already in this account?
        #
        x = self.UTILS.get_element(*DOM.GLOBAL.app_head)
        if x.text == p_address:
            # Already here - just go to the Inbox.
            self.goto_folder_from_list("Inbox")
            return True
        
        #
        # We're not in this account already, so let's look for it.
        #
        x = self.UTILS.get_element(*DOM.Email.goto_accounts_btn)
        self.marionette.tap(x)
        
        self.parent.wait_for_element_displayed('xpath', DOM.GLOBAL.app_head_specific % "Accounts")
        
        #
        # Check if it's already set up.
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


    #
    # Remove current email account and restart the application.
    #
    def remove_accounts_and_restart(self):
        x = self.UTILS.get_element(*DOM.Email.settings_menu_btn)
        self.marionette.tap(x)
        
        x = self.UTILS.get_element(*DOM.Email.settings_set_btn)
        self.marionette.tap(x)
        
        self.parent.wait_for_element_displayed('xpath', DOM.GLOBAL.app_head_specific % "Mail settings")
        
        #
        # Remove each email address listed ...
        #
        x = self.UTILS.get_elements('class name', 'tng-account-item-label list-text')
        for i in x:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.reportComment("i: " + i.text)
                self.marionette.tap(i)
                self.parent.wait_for_element_displayed('xpath', DOM.GLOBAL.app_head_specific % i.text)
                
                # Delete.
                delacc = self.UTILS.get_element(*DOM.Email.settings_del_acc_btn)
                self.marionette.tap(delacc)
                
                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.get_element(*DOM.Email.settings_del_conf_btn)
                self.marionette.tap(delconf)
                
                # Wait for .... something ...??
        
        #
        # Now relaunch the app.
        #
        self.launch()
    
    #
    # Login.
    #
    def setupAccount(self, p_user, p_email, p_pass):
        #
        # If we've just started out, email will open directly to "New account").
        #
        x = self.marionette.find_element(*DOM.GLOBAL.app_head)
        if x.text != "New account":
            #
            # We have at least one emali account setup,
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(p_email):
                return
        
            #
            # It's not setup already, so prepare to set it up!
            #
            x = self.UTILS.get_element(*DOM.Email.settings_set_btn)
            self.marionette.tap(x)
            
            x = self.UTILS.get_element(*DOM.Email.settings_add_account_btn)
            self.marionette.tap(x)

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        u = self.UTILS.get_element(*DOM.Email.username)
        e = self.UTILS.get_element(*DOM.Email.email_addr)
        p = self.UTILS.get_element(*DOM.Email.password)

        if p_user != "":
            u.send_keys(p_user)
        if p_email != "":
            e.send_keys(p_email)
        if p_pass != "":
            p.send_keys(p_pass)
            
        btn = self.UTILS.get_element(*DOM.Email.login_next_btn)
        self.marionette.tap(btn)
        
        self.parent.wait_for_element_displayed(*DOM.Email.sup_header)
        
        #
        # Click the 'continue ...' button.
        #
        x = self.UTILS.get_element(*DOM.Email.sup_continue_btn)
        self.marionette.tap(x)
        
        self.waitForDone()
        
    
    #
    # Compose and send a new email.
    #
    def send_new_email(self, p_target, p_subject, p_message):
        x = self.UTILS.get_element(*DOM.Email.compose_msg_btn)
        self.marionette.tap(x)
        
        #
        # Wait for 'compose message' header.
        #
        x = self.UTILS.get_element('xpath', DOM.GLOBAL.app_head_specific % "Compose message")
        self.UTILS.TEST(x.is_displayed(), 
            "Failed to arrive at 'compose' screen after clicking to compose a new email.", True)
        
        #
        # Put items in the corresponsing fields.
        #
        msg_to      = self.UTILS.get_element(*DOM.Email.compose_to)
        msg_subject = self.UTILS.get_element(*DOM.Email.compose_subject)
        msg_msg     = self.UTILS.get_element(*DOM.Email.compose_msg)
        
        msg_to.send_keys(p_target)
        msg_subject.send_keys(p_subject)
        msg_msg.send_keys(p_message)
        
        #
        # Send the message.
        #
        x = self.UTILS.get_element(*DOM.Email.compose_send_btn)
        self.marionette.tap(x)
        
        self.waitForDone()
            
        #TEST compose_send_failed_msg - don't know how to swich to this frame!

        #
        # Wait for inbox to re-appear.
        #
        self.parent.wait_for_element_displayed('xpath', DOM.GLOBAL.app_head_specific % "Inbox")
        
    #
    # Open a specific mail folder (must be called from "Inbox").
    #
    def openMailFolder(self, p_folderName):
        x = self.UTILS.get_element(*DOM.Email.settings_menu_btn)
        self.marionette.tap(x)
        
        #
        # When we're looking at the folders screen ...
        #
        self.parent.wait_for_element_displayed(*DOM.Email.folderList_header)

        #
        # ... click on the folder were after.
        #
        self.goto_folder_from_list(p_folderName)
        
        #
        # Wait a while for everything to finish populating.
        #
        time.sleep(5)
            
        
    #
    # Assumes we are in the required folder.
    #
    def openMsg(self, p_subject):
        # ROY - try and get this nightmare working SOMEHOW!!!

        if self.emailIsInFolder(p_subject):
        
            #
            # After trying almost everything (including "//*[text()="!)
            # I'm resorting to brute force!!
            #
            z = self.marionette.find_elements('xpath', "//span")
            for i in z:
                if i.text == p_subject:
                    i.click()
                    return True
            
            return False
        
        else:
            self.UTILS.reportError("Unable to find a message with the subject '"  + p_subject + "' in this folder.")
            return False


        #x = self.marionette.find_elements('class name', 'msg-header-item')
        #for i in x:
            #if i.is_displayed():
                ##y = i.find_element('class name', 'msg-header-subject')
                ##if y.text == p_subject:
                #i.click()
                #return True
        #return False
        

            
        #try:
            #x = self.UTILS.get_element("xpath", "//span[text()='%s']" % p_subject)

            ##
            ## For some reason this link has to be clicked, NOT tapped
            ## (imagine how much time I wasted figuring that out!)!
            ##
            #x.click()
            #return True
        #except:
            #self.UTILS.reportError("Email with subject '" + p_subject + "' not found.")
            #return False
        
        ##
        ## The subject part doesn't always do anything when you tap it, so I need the
        ## parent link as well.
        ##
        #subject_areas   = self.UTILS.get_elements(*DOM.Email.folder_subject_list)
        #for i in subject_areas:
            #if i.text == p_subject:
                ##
                ## For some reason this link has to be clicked, NOT tapped
                ## (imagine how much time I wasted figuring that out!)!
                ##
                ##i.click()
                #self.marionette.tap(i)
                    
                #try: self.parent.wait_for_element_displayed(*DOM.Email.open_email_subject)
                #except:
                    #self.UTILS.TEST(1==2, "Found the email but it won't open!", True)
                    #return False
                #else:
                    #return True
        
        #self.UTILS.reportError("Email with subject \"" + p_subject + "\" not found.")
        #return False
    
    #
    # Verify an email is in this folder with the expected subject.
    #
    def emailIsInFolder(self, p_subject):
        #
        # After trying almost everything (including //span[text()=)
        # I'm resorting to brute force!!
        #
        z = self.marionette.find_elements('xpath', "//span")
        for i in z:
            if i.text == p_subject:
                return True
        
        return False
