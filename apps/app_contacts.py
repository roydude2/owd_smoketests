import DOM, time
from gaiatest   import GaiaTestCase
from utils      import UTILS
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
        self.UTILS      = UTILS(self)  
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS

    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Contacts')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay")

    def getContactFields(self):
        #
        # Return 3-d array of contact details (from view or edit contacts screen
        # - the identifiers should be the same ... *should* ...)
        # 
        # (Just makes the code a little simpler when you use this.)
        #
        
        return {
        'givenName' : self.UTILS.getElement(DOM.Contacts.given_name_field, "Given name field"),
        'familyName': self.UTILS.getElement(DOM.Contacts.family_name_field, "Family name field"),
        'tel'       : self.UTILS.getElement(DOM.Contacts.phone_field, "Phone number field"),
        'email'     : self.UTILS.getElement(DOM.Contacts.email_field, "Email field"),
        'street'    : self.UTILS.getElement(DOM.Contacts.street_field, "Street field"),
        'zip'       : self.UTILS.getElement(DOM.Contacts.zip_code_field, "Zip code field"),
        'city'      : self.UTILS.getElement(DOM.Contacts.city_field, "City field"),
        'country'   : self.UTILS.getElement(DOM.Contacts.country_field, "Country field"),
        'comment'   : self.UTILS.getElement(DOM.Contacts.comment_field, "Comment field")
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

    def checkMatch(self, p_el, p_val, p_name):
        #
        # Test for a match between an element and a string
        # (found I was doing this rather a lot so it's better in a function).
        #
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
#        x = self.marionette.find_element("id", "thumbnail-photo")
        x = self.UTILS.getElement(("id", "thumbnail-photo"), "'Add picture' link")
        self.marionette.tap(x)
        time.sleep(2)
        
        # Switch to the 'make a choice' iframe.
        self.marionette.switch_to_frame()
        
        # Choose to get a picture from the Gallery.
        x = self.UTILS.getElement(("link text", "Gallery"), "Gallery link")
        self.marionette.tap(x)
#        boolOK = True
#        try:
#            x = self.marionette.find_element("link text", "Gallery")
#            self.marionette.tap(x)
#        except:
#            boolOK = False
#
#        self.UTILS.TEST(boolOK, "Can select import picture from Gallery app.")
        
        time.sleep(1)
        
        # Switch to Gallery iframe.
        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)
        
        # Select the thumbnail (assume it's the only one).
        x = self.UTILS.getElement(DOM.Contacts.picture_thumbnail, "Thumbnail for picture")
        self.marionette.tap(x)
            
        time.sleep(1)
        
        # Tap 'crop done' button.
        boolOK = True
        try:
            x = self.UTILS.getElement(DOM.Contacts.picture_crop_done_btn, "Crop 'done' button")
            self.marionette.tap(x)
        except:
            boolOK = False

        self.UTILS.TEST(boolOK, "Can finish cropping the picture and return to Contacts app.")
            
        time.sleep(1)
        
        # Back to contacts app iframe.
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

         

    def createNewContact(self, p_contact, p_addImage=False):
        #
        # Create a contact using the UI.
        #
        
        #
        # First make sure we're in the right place.
        #
#        viewAllHeader = self.marionette.find_element(*DOM.Contacts.view_all_header)
        viewAllHeader = self.UTILS.getElement(DOM.Contacts.view_all_header, "'View all contacts' header", False)
        if not viewAllHeader.is_displayed():
            #
            # Header isn't present, so we're not running yet.
            #
            self.launch()
            
        #
        # Click Create new contact from the view all screen.
        #
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        add_new_contact = self.UTILS.getElement(DOM.Contacts.add_contact_button, "'Add new contact' button")
        
        self.marionette.tap(add_new_contact)
        
        #
        # Enter details for new contact.
        #
        self.UTILS.waitForElements(DOM.Contacts.add_contact_header, "Add contact header")
        
        if p_addImage:
            # Put the image on the contact.
            self.addImageToContact()
        
        # Put the contact details into each of the fields.
        self.populateFields(p_contact)
        
        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        self.marionette.tap(done_button)
        
        # Wait for the 'view all contacts' header to be displayed.
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        
        # Now check the contact's name is displayed here too.
        x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))
        self.UTILS.waitForElements(x, "Contact '" + p_contact['name'] + "'")
        
        if p_addImage:
            #
            # Verify that the contact's image is displayed.
            #
            x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contact list", False)
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
#        try:
#            contact_found = self.marionette.find_element("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))
#        except:
#            self.UTILS.logResult(False, "'" + p_contact['name'] + "' is found in the contacts list!")
#            return 0 # (leave the function)

        #
        # TEST: try to click the contact name in the contacts list.
        #
        x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))
        contact_found = self.UTILS.getElement(x, "Contact '" + p_contact['name'] + "'")
        self.marionette.tap(contact_found)
        
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

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
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        self.marionette.tap(x)
        
        self.UTILS.waitForElements(DOM.Contacts.settings_header, "Settings header")
        
    def checkViewContactDetails(self, p_contact, p_imageCheck = False):
        #
        # Validate the details of a contact in the 'view contact' screen.
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact)
        
        if p_imageCheck:
            #
            # Verify that an image is displayed.
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
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        self.marionette.tap(editBTN)
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' screen header")

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
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        self.marionette.tap(editBTN)
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")

        #
        # Enter the new contact details.
        #
        self.populateFields(p_contact_new)
        
        #
        # Save the changes
        #
        updateBTN = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        self.marionette.tap(updateBTN)

        #
        # Return to the contact list screen.
        #
        backBTN = self.UTILS.getElement(DOM.Contacts.details_back_button, "Details 'back' button")
        self.marionette.tap(backBTN)
        
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "'View all contacts' screen header")

    def tapLinkContact(self):
        #
        # Press the 'Link contact' button in the view contact details screen.
        #
        
        #
        # NOTE: there is more than one button with this ID, so make sure we use the right one!
        # (One of them isn't visible, so we need to check for visibility this way or the
        # 'invisible' one will cause 'getElements()' to fail the test).
        #
        time.sleep(2)
#        x = self.marionette.find_elements(*DOM.Contacts.link_button)
        x = self.UTILS.getElements(DOM.Contacts.link_button, "Link contact button", False)
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
        self.UTILS.waitForElements(DOM.Facebook.friends_header, "Facebook friends screen header")
        time.sleep(2)
        
    def enableFBImport(self):
        #
        # Enable fb import.
        #

        self.tapSettingsButton()
        x = self.UTILS.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")        
        self.marionette.tap(x)
        
        #
        # Were we already connected to facebook?
        #
        try:
            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

            #
            # If we get to here, we're already logged into facebook - remove fb data
            # so we can proceed with this part of the test from sratch.
            #
            # (You don't want this to validate properly - if it's not there it's okay so use
            # 'marionette.find_element' or the test will fail if the button's absent.)
            x = self.marionette.find_element('xpath', "//button[text()='Remove']")
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
            
            x = self.UTILS.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
            self.marionette.tap(x)
            
        except:
            #
            # We weren't logged into facebook, so continue.
            #
            pass

        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        time.sleep(2) # Just to be sure!

