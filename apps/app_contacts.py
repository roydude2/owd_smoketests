import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppContacts(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self, 00)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS


    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)


    def getContactFields(self):
        #
        # Return 3-d array of contact details (from view or edit contacts screen
        # - the identifiers should be the same ... *should* ...)
        # 
        # (Just makes the code a little simpler when you use this.)
        #
        
        return {
        'givenName' : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.given_name_field")),
        'familyName': self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.family_name_field")),
        'tel'       : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.phone_field")),
        'email'     : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.email_field")),
        'street'    : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.street_field")),
        'zip'       : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.zip_code_field")),
        'city'      : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.city_field")),
        'country'   : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.country_field")),
        'comment'   : self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.comment_field"))
        }
        
    def replaceStr(self, p_field, p_str):
        #
        # Replace text in a field (as opposed to just appending to it).
        #
        p_field.clear()
        p_field.send_keys(p_str)

    def populateFields(self, p_contact):
        #
        # Put the contact details into the fields (assumes you are in the correct
        # screen already since this could be create or edit).
        #
        contFields = self.getContactFields()
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.replaceStr(contFields['givenName'  ] , p_contact["givenName"])
        self.replaceStr(contFields['familyName' ] , p_contact["familyName"])
        self.replaceStr(contFields['tel'        ] , p_contact["tel"]["value"])
        self.replaceStr(contFields['email'      ] , p_contact["email"]["value"])
        self.replaceStr(contFields['street'     ] , p_contact["adr"]["streetAddress"])
        self.replaceStr(contFields['zip'        ] , p_contact["adr"]["postalCode"])
        self.replaceStr(contFields['city'       ] , p_contact["adr"]["locality"])
        self.replaceStr(contFields['country'    ] , p_contact["adr"]["countryName"])
        self.replaceStr(contFields['comment'    ] , p_contact["comment"])


    def verifyFieldContents(self, p_contact):
        #
        # Verify the contents of the contact fields in this screen (assumes
        # you are in the correct screen since this could be view or edit).
        #

        #self.UTILS.reportComment("Not testing email field at the moment (it turns the screen off when automated!).")

        contFields = self.getContactFields()      # Get the contact's fields again.
        
        self.UTILS.checkMatch(contFields['givenName' ] , "value", p_contact['givenName']            , "given name")
        self.UTILS.checkMatch(contFields['familyName'] , "value", p_contact['familyName']           , "family name")
        self.UTILS.checkMatch(contFields['tel'       ] , "value", p_contact['tel']['value']         , "telephone")
        self.UTILS.checkMatch(contFields['email'     ] , "value", p_contact['email']['value']       , "email")
        self.UTILS.checkMatch(contFields['street'    ] , "value", p_contact['adr']['streetAddress'] , "street")
        self.UTILS.checkMatch(contFields['zip'       ] , "value", p_contact['adr']['postalCode']    , "zip")
        self.UTILS.checkMatch(contFields['city'      ] , "value", p_contact['adr']['locality']      , "city")
        self.UTILS.checkMatch(contFields['country'   ] , "value", p_contact['adr']['countryName']   , "country")
        self.UTILS.checkMatch(contFields['comment'   ] , "value", p_contact['comment']              , "comment")


    def createNewContact(self, p_contact):
        #
        # Create a contact using the UI.
        #
        
        #
        # First make sure we're in the right place.
        #
        viewAllHeader = self.marionette.find_element(*self.UTILS.verify("DOM.Contacts.view_all_header"))
        if not viewAllHeader.is_displayed():
            self.launch()
            
        #
        # Click Create new contact from the view all screen.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.view_all_header"))
        add_new_contact = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.add_contact_button"))
        
        self.marionette.tap(add_new_contact)
        
        #
        # Enter details for new contact.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.add_contact_header"))
        
        # Put the contact details into each of the fields.
        self.populateFields(p_contact)
        
        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.done_button"))
        self.marionette.tap(done_button)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.view_all_header"))
        
        # For some reason the new contact doesn't always appear imediately.
        #time.sleep(5)
        self.wait_for_element_displayed("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))


    def viewContact(self, p_contact):
        #
        # Navigate to the 'view details' screen for a contact (assumes we ae in the
        # 'view all contacts' screen).
        #
        
        #
        # Find the name of our contact in the contacts list.
        #
        try:
            contact_found = self.marionette.find_element("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))
        except:
            self.UTILS.reportError("Could not find '" + p_contact['name'] + "' in the contacts list!")
            return 0 # (leave the function)
        
        #
        # TEST: try to click the contact name in the contacts list.
        #
        try:
            self.marionette.tap(contact_found)
        except:
            self.UTILS.reportError("Could not tap on '" + p_contact['name'] + "' in contacts list!")
            return 0 # (leave the function)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.view_details_title"))

        # 
        # TEST: Correct contact name is in the page header.
        #
        self.UTILS.TEST(self.UTILS.headerFound(p_contact['name']), 
            "'View contact' screen header was not '" + p_contact["name"] + "'.")
            
        time.sleep(2)
    
    def pressLinkContact(self):
        #
        # Press the 'Link contact' button in the view contact details screen.
        #
        
        #
        # NOTE: there is more than one button with this ID, so make sure we use the right one!
        #
        time.sleep(2)
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Contacts.link_button"))
        for i in x:
            if i.is_displayed():
                self.marionette.tap(i)
                break
        
        #
        # We need a long pause to be sure the frames are all complete.
        #
        time.sleep(8)
        
        #
        # Travel through the frames to the one we need for the import page.
        #
        self.marionette.switch_to_frame()
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Facebook.fb_friends_iframe_1)
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Facebook.fb_friends_iframe_2)
        time.sleep(2)

        #
        # Wait for the fb friends page to start.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Facebook.fb_friends_header"))
        time.sleep(2)
        
    
    def tapSettingsButton(self):
        #
        # Tap the settings button.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.settings_button"))
        self.marionette.tap(x)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.settings_header"))
        
    def tapLinkButton(self):
        #
        # Tap the link button to go to facebook.
        #
        
        #
        # There's more than one element with the id "link_button"
        # (and matching on text() didn't work)!
        #
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Contacts.link_button"))
        for i in x:
            if i.is_displayed():
                if i.text == "Link contact":
                    i.click()
                    self.marionette.tap(i)

    def checkViewContactDetails(self, p_contact):
        #
        # Validate the details of a contact in the 'view contact' screen.
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact)
        
        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact)

    def checkEditContactDetails(self, p_contact):
        #
        # Validate the details of a contact in the 'view contact' screen.
        #
        editBTN = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.edit_details_button"))
        self.marionette.tap(editBTN)
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.edit_contact_header"))

        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact)

    def editContact(self, p_contact_curr, p_contact_new):
        #
        # Replace the details of one contact with another via the edit screen.
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact_curr)
                
        #
        # Tap the Edit button to go to the edit details page.
        #
        editBTN = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.edit_details_button"))
        self.marionette.tap(editBTN)
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.edit_contact_header"))

        #
        # Enter the new contact details.
        #
        self.populateFields(p_contact_new)
        
        #
        # Save the changes
        #
        updateBTN = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.edit_update_button"))
        self.marionette.tap(updateBTN)

        #
        # Return to the contact list screen.
        #
        backBTN = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.details_back_button"))
        self.marionette.tap(backBTN)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.view_all_header"))

    def fb_importAll(self):
        #
        # Import all contacts.
        #
        
        #
        # Tap 'Update imported friends' button.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.settings_import_fb"))        
        self.marionette.tap(x)
        
        #
        # Travel through the frames to the one we need for the import page.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.fb_friends_iframe_1)
        self.UTILS.switchToFrame(*DOM.Facebook.fb_friends_iframe_2)

        #
        # Wait for the fb friends page to start.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Facebook.fb_friends_header"))
        time.sleep(2)
        
        #
        # Get the count of friends that will be imported.
        #
        x = self.UTILS.get_elements(*self.UTILS.verify("DOM.Facebook.fb_friends_list"))
        friend_count = len(x)
        
        #
        # Tap "Select all".
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.fb_friends_select_all"))
        self.marionette.tap(x)
        
        #
        # Tap "Import".
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Facebook.fb_friends_import"))
        self.marionette.tap(x)
        
        #
        # Return the number of friends we imported.
        #
        return friend_count
        
        
        
    # Facebook have now added a 'captcha' to the login process here, so we
    # can no-longer automate this part.
    # I'm leaving this here though, just in case they decide to remove the
    # captcha in the future.
    ##
    ## Enable fb import.
    ##
    #def fb_enable(self):
        #self.tapSettingsButton()
        #x = self.UTILS.get_element(*DOM.Contacts.settings_fb_enable)        
        #self.marionette.tap(x)
        
        ##
        ## Were we already connected to facebook?
        ##
        #try:
            #x = self.UTILS.get_element('xpath', "//button[text()='Remove']")
        #except:
            #pass
        #else:
            ##
            ## We are already logged into facebook - remove fb data
            ## so we can proceed with this part of the test from sratch.
            ##
            #self.marionette.tap(x)
            #time.sleep(5)
            
            ##
            ## Now click the 'enable facebook' button again.
            ##
            #self.UTILS.connect_to_iframe("app://communications.gaiamobile.org/contacts/index.html")
            #x = self.UTILS.get_element(*DOM.Contacts.settings_fb_enable)
            #self.marionette.tap(x)
            
        ##
        ## Give facebook time to load, then connect to the iframe with src=""
        ## to see the facebook screen.
        ##
        #time.sleep(2) # Just to be sure!

    ##
    ## Log into facebook.
    ##
    #def fb_login(self, p_user, p_pass):
        ##
        ## Get to the facebook login frame.
        ##
        #self.marionette.switch_to_frame()
        #self.UTILS.connect_to_iframe("")
        
        #x = self.UTILS.get_element(*DOM.Facebook.email)
        #x.send_keys(p_user)
        
        #x = self.UTILS.get_element(*DOM.Facebook.password)
        #x.send_keys(p_pass)

        #x = self.UTILS.get_element(*DOM.Facebook.login_button)
        #self.marionette.tap(x)
        
        #time.sleep(3)
        
        
