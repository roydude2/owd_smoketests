import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppFacebook(GaiaTestCase):
    
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


    def LinkContact(self, p_contactEmail):
        #
        # After clicking the link contact button, use this to click on a contact.
        #
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Facebook.link_friends_list"))
        
        email = False
        
        for i in x:
            if i.is_displayed():
                #
                # Keep the name and email detais for this contact.
                #
                thisContact = i.find_elements("tag name", "p")[1]
                
                if thisContact.text == p_contactEmail:
                    self.marionette.tap(i)
                    email = p_contactEmail
                    break

        self.UTILS.TEST(email, "Desired link contact's email address is displayed.")
        
        if email:
            self.UTILS.logComment("Linked FB contact email: " + email + ".")
        
        #
        # Switch back and wait for contact details page to re-appear.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.friends_iframe_1)

    def tapUpdateImportedFriends(self):
        #
        # Tap 'Update imported friends' button.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.settings_import_fb"))        
        self.marionette.tap(x)
        

    def importAll(self):
        #
        # Import all contacts after enabling fb via Contacts Settings.
        #
        
        #
        # Travel through the frames to the one we need for the import page.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.friends_iframe_1)
        self.UTILS.switchToFrame(*DOM.Facebook.friends_iframe_2)

        #
        # Wait for the fb friends page to start.
        #
        self.UTILS.waitForDisplayed(20, "facebook friends header displayed.", True, DOM.Facebook.friends_header)
#        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Facebook.friends_header"))
        time.sleep(2)
        
        #
        # Get the count of friends that will be imported.
        #
        x = self.UTILS.get_elements(*self.UTILS.verify("DOM.Facebook.friends_list"))
        friend_count = len(x)
        
        #
        # Tap "Select all".
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.friends_select_all"))
        self.marionette.tap(x)
        
        #
        # Tap "Import".
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.friends_import"))
        self.marionette.tap(x)
        
        #
        # Switch back to the contacts frame.
        #
        # (The 'importing ..' splash screen that appears confuses the frame switch
        # so the simplest thing is to just wait for a long time to make sure it's
        # gone.)
        #
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Return the number of friends we imported.
        #
        return friend_count
    
    def login(self, p_user, p_pass):
        #
        # Log into facebook.
        #

        #
        # Get to the facebook login frame.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.import_frame)
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.email"))
        x.send_keys(p_user)
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.password"))
        x.send_keys(p_pass)
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.login_button"))
        self.marionette.tap(x)
        
        time.sleep(3)