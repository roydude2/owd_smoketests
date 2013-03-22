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
        self.parent     = p_parent

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self)        
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

    #
    # Test for a match between an element and a string
    # (found I was doing this rather a lot so it's better in a function).
    #
    def checkMatch(self, p_el, p_val, p_name):
        test_str = str(p_el.get_attribute("value"))

        self.UTILS.TEST(
            (test_str == p_val),
            p_name + " = \"" + p_val + "\" (it was \"" + test_str + "\")."
            )

    def verifyFieldContents(self, p_contact):
        #
        # Verify the contents of the contact fields in this screen (assumes
        # you are in the correct screen since this could be view or edit).
        #
        contFields = self.getContactFields()      # Get the contact's fields again.
        
        self.checkMatch(contFields['givenName' ] , p_contact['givenName']            , "Given name")
        self.checkMatch(contFields['familyName'] , p_contact['familyName']           , "Family name")
        self.checkMatch(contFields['tel'       ] , p_contact['tel']['value']         , "Telephone")
        self.checkMatch(contFields['email'     ] , p_contact['email']['value']       , "Email")
        self.checkMatch(contFields['street'    ] , p_contact['adr']['streetAddress'] , "Street")
        self.checkMatch(contFields['zip'       ] , p_contact['adr']['postalCode']    , "Zip")
        self.checkMatch(contFields['city'      ] , p_contact['adr']['locality']      , "City")
        self.checkMatch(contFields['country'   ] , p_contact['adr']['countryName']   , "Country")
        self.checkMatch(contFields['comment'   ] , p_contact['comment']              , "COMMENTS")


    def addImageToContact(self):
        #
        # Adds an image for this contact from the gallery
        # (assumes we're already in the 'new contact' screen).
        #
        
        # Upload an image into the gallery.
        self.parent.push_resource('contact_face.jpg', destination='DCIM/100MZLLA')

        #
        # Click the 'add picture' link.
        #
        x = self.marionette.find_element("id", "thumbnail-photo")
        self.marionette.tap(x)
        time.sleep(2)
        
        # Switch to the 'make a choice' iframe.
        self.marionette.switch_to_frame()
        
        # Choose to get a picture from the Gallery.
        boolOK = True
        try:
            x = self.marionette.find_element("link text", "Gallery")
            self.marionette.tap(x)
        except:
            boolOK = False

        self.UTILS.TEST(boolOK, "Can select import picture from Gallery app.")
            
        time.sleep(1)
        
        # Switch to Gallery iframe.
        self.UTILS.switchToFrame("src", "app://gallery.gaiamobile.org/index.html#pick")
        
        # Select the thumbnail (assume it's the only one).
        boolOK = True
        try:
            x = self.marionette.find_element("xpath", "//*[@id='thumbnails']/li[1]")
            self.marionette.tap(x)
        except:
            boolOK = False

        self.UTILS.TEST(boolOK, "Can select picture in Gallery app.")
            
        time.sleep(1)
        
        # Tap 'crop done' button.
        boolOK = True
        try:
            x = self.marionette.find_element("id", "crop-done-button")
            self.marionette.tap(x)
        except:
            boolOK = False

        self.UTILS.TEST(boolOK, "Can finish cropping the picture and return to Contacts app.")
            
        time.sleep(1)
        
        # Back to contacts app iframe.
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame("srC", "app://communications.gaiamobile.org/contacts/index.html")

         

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
        
        # Put the image on the contact.
        self.addImageToContact()
        
        # Put the contact details into each of the fields.
        self.populateFields(p_contact)
        
        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.done_button"))
        self.marionette.tap(done_button)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.view_all_header"))
        
        self.wait_for_element_displayed("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))
        
        #
        # Verify that the contact's image is displayed.
        #
        x = self.marionette.find_elements("xpath", "//li[@class='contact-item']")
        for i in x:
            try:
                i.find_element("xpath", "//p[@data-order='%s']" % p_contact['name'].replace(" ",""))
            except:
                pass
            else:
                #
                # This is our contact - try and get the image.
                #
                boolOK = True
                try:
                    x = i.find_element("xpath", "//img")
                    self.UTILS.TEST("blob" in x.get_attribute("src"), "Contact image present in 'all contacts' screen.")
                except:
                    boolOK = False
                
                self.UTILS.TEST(boolOK, "An image is present for this contact in all contacts screen.")
                


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
            self.UTILS.logResult(False, "'" + p_contact['name'] + "' is found in the contacts list!")
            return 0 # (leave the function)
        
        #
        # TEST: try to click the contact name in the contacts list.
        #
        try:
            self.marionette.tap(contact_found)
        except:
            self.UTILS.logResult(False, "Able to tap on '" + p_contact['name'] + "' in contacts list!")
            return 0 # (leave the function)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.view_details_title"))

        # 
        # TEST: Correct contact name is in the page header.
        #
        self.UTILS.TEST(self.UTILS.headerCheck(p_contact['name']), 
            "'View contact' screen header = '" + p_contact["name"] + "'.")
            
        time.sleep(2)
    
    def tapSettingsButton(self):
        #
        # Tap the settings button.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Contacts.settings_button"))
        self.marionette.tap(x)
        
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Contacts.settings_header"))
        
    def checkViewContactDetails(self, p_contact):
        #
        # Validate the details of a contact in the 'view contact' screen.
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact)
        
        #
        # Verify that the contact image is displayed.
        #
        x = self.marionette.find_element("id", "cover-img")
        x_style = x.get_attribute("style")
        self.UTILS.TEST("blob" in x_style, "Contact's image contains 'something' in contact details screen.")

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

    def tapLinkContact(self):
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
        time.sleep(5)
        
        #
        # Travel through the frames to the one we need for the import page.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.friends_iframe_1)
        self.UTILS.switchToFrame(*DOM.Facebook.friends_iframe_2)

        #
        # Wait for the fb friends page to start.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Facebook.friends_header"))
        time.sleep(2)
        
    #
    # Facebook have now added a 'captcha' to the login process here, so we
    # can no-longer automate this part.
    # I'm leaving this here though, just in case they decide to remove the
    # captcha in the future.
    #
    # Enable fb import.
    #
    def enableFBImport(self):
        self.tapSettingsButton()
        x = self.UTILS.get_element(*DOM.Contacts.settings_fb_enable)        
        self.marionette.tap(x)
        
        #
        # Were we already connected to facebook?
        #
        x = self.UTILS.get_element('xpath', "//button[text()='Remove']")
        if x:
            #
            # We were already logged into facebook - remove fb data
            # so we can proceed with this part of the test from sratch.
            #
            self.marionette.tap(x)
            time.sleep(5)
            
            #
            # Now click the 'enable facebook' button again.
            #
            # For some reason I need to relaunch the Contacts app first.
            # If I don't then after I log in again the 'Please hold on ...'
            # message stays forever.
            # (This is only a problem when automating - if you do this
            # manually it works fine.)
            #
            self.launch()
            self.tapSettingsButton()
            
            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
            
            x = self.UTILS.get_element(*DOM.Contacts.settings_fb_enable)
            self.marionette.tap(x)

        time.sleep(2) # Just to be sure!

