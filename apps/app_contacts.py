from apps import DOM
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.testUtils  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.app = self.parent.apps.launch('Contacts')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)


    #
    # Return 3-d array of contact details (from view or edit contacts screen
    # - the identifiers should be the same ... *should* ...)
    # 
    # (Just makes the code a little simpler when you use this.)
    #
    def getContactFields(self):
        
        return {
        'givenName' : self.testUtils.get_element(*DOM.Contacts.given_name_field),
        'familyName': self.testUtils.get_element(*DOM.Contacts.family_name_field),
        'tel'       : self.testUtils.get_element(*DOM.Contacts.phone_field),
        'email'     : self.testUtils.get_element(*DOM.Contacts.email_field),
        'street'    : self.testUtils.get_element(*DOM.Contacts.street_field),
        'zip'       : self.testUtils.get_element(*DOM.Contacts.zip_code_field),
        'city'      : self.testUtils.get_element(*DOM.Contacts.city_field),
        'country'   : self.testUtils.get_element(*DOM.Contacts.country_field),
        'comment'   : self.testUtils.get_element(*DOM.Contacts.comment_field)
        }
        
    #
    # Replace text in a field (as opposed to just appending to it).
    #
    def replaceStr(self, p_field, p_str):
        p_field.clear()
        p_field.send_keys(p_str)

    #
    # Put the contact details into the fields (assumes you are in the correct
    # screen already since this could be create or edit).
    #
    def populateFields(self, p_contact):
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
    # Verify the contents of the contact fields in this screen (assumes
    # you are in the correct screen since this could be view or edit).
    #
    def verifyFieldContents(self, p_contact):

        #self.testUtils.reportComment("Not testing email field at the moment (it turns the screen off when automated!).")

        contFields = self.getContactFields()      # Get the contact's fields again.
        
        self.testUtils.testMatch(contFields['givenName' ] , "value", p_contact['givenName']            , "given name")
        self.testUtils.testMatch(contFields['familyName'] , "value", p_contact['familyName']           , "family name")
        self.testUtils.testMatch(contFields['tel'       ] , "value", p_contact['tel']['value']         , "telephone")
        self.testUtils.testMatch(contFields['email'     ] , "value", p_contact['email']['value']       , "email")
        self.testUtils.testMatch(contFields['street'    ] , "value", p_contact['adr']['streetAddress'] , "street")
        self.testUtils.testMatch(contFields['zip'       ] , "value", p_contact['adr']['postalCode']    , "zip")
        self.testUtils.testMatch(contFields['city'      ] , "value", p_contact['adr']['locality']      , "city")
        self.testUtils.testMatch(contFields['country'   ] , "value", p_contact['adr']['countryName']   , "country")
        self.testUtils.testMatch(contFields['comment'   ] , "value", p_contact['comment']              , "comment")


    def createNewContact(self, p_contact):
        #
        # First make sure we're in the right place.
        #
        viewAllHeader = self.marionette.find_element(*DOM.Contacts.view_all_header)
        if not viewAllHeader.is_displayed():
            self.launch()
            
        #
        # Click Create new contact from the view all screen.
        #
        self.parent.wait_for_element_displayed(*DOM.Contacts.view_all_header)
        add_new_contact = self.testUtils.get_element(*DOM.Contacts.add_contact_button)
        
        self.testUtils.clickNTap(add_new_contact)
        
        #
        # Enter details for new contact.
        #
        self.parent.wait_for_element_displayed(*DOM.Contacts.add_contact_header)
        
        # Put the contact details into each of the fields.
        self.populateFields(p_contact)
        
        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.testUtils.get_element(*DOM.Contacts.done_button)
        self.testUtils.clickNTap(done_button)
        
        self.parent.wait_for_element_displayed(*DOM.Contacts.view_all_header)
        
        # For some reason the new contact doesn't always appear imediately.
        self.parent.wait_for_element_displayed("link text", p_contact['name'])

    #
    # Navigate to the 'view details' screen for a contact (assumes we ae in the
    # 'view all contacts' screen).
    #
    def viewContact(self, p_contact):
        #
        # Find the name of our contact in the contacts list.
        #
        try:
            contact_found = self.marionette.find_element("link text", p_contact['name'])
        except:
            self.testUtils.reportError("Could not find '" + p_contact['name'] + "' in the contacts list!")
            return 0 # (leave the function)
        
        #
        # TEST: try to click the contact name in the contacts list.
        #
        try: 
            self.testUtils.clickNTap(contact_found)
        except:
            self.testUtils.reportError("Could not tap on '" + p_contact['name'] + "' in contacts list!")
            return 0 # (leave the function)
        
        self.parent.wait_for_element_displayed(*DOM.Contacts.view_details_title)

        # 
        # TEST: Correct contact name is in the page header.
        #
        self.testUtils.TEST(self.testUtils.headerFound(p_contact['name']), 
            "'View contact' screen header was not '" + p_contact["name"] + "'.")
        


    #
    # Validate the details of a contact in the 'view contact' screen.
    #
    def checkViewContactDetails(self, p_contact):
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact)
        
        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact)

    #
    # Validate the details of a contact in the 'view contact' screen.
    #
    def checkEditContactDetails(self, p_contact):
        editBTN = self.testUtils.get_element(*DOM.Contacts.edit_details_button)
        self.testUtils.clickNTap(editBTN)
        self.parent.wait_for_element_displayed(*DOM.Contacts.edit_contact_header)

        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact)

    #
    # Replace the details of one contact with another via the edit screen.
    #
    def editContact(self, p_contact_curr, p_contact_new):
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact_curr)
                
        #
        # Tap the Edit button to go to the edit details page.
        #
        editBTN = self.testUtils.get_element(*DOM.Contacts.edit_details_button)
        self.testUtils.clickNTap(editBTN)
        self.parent.wait_for_element_displayed(*DOM.Contacts.edit_contact_header)

        #
        # Enter the new contact details.
        #
        self.populateFields(p_contact_new)
        
        #
        # Save the changes
        #
        updateBTN = self.testUtils.get_element(*DOM.Contacts.edit_update_button)
        self.testUtils.clickNTap(updateBTN)

        #
        # Return to the contact list screen.
        #
        backBTN = self.testUtils.get_element(*DOM.Contacts.details_back_button)
        self.testUtils.clickNTap(backBTN)
        
        self.parent.wait_for_element_displayed(*DOM.Contacts.view_all_header)
