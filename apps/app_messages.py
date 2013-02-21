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
        self.app = self.parent.apps.launch('Messages')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    #
    # Create and send a message (assumes we are in a new 'create new message'
    # screen with the destination number filled in already).
    #
    def enterSMSMsg(self, p_msg):
        msgArea = self.testUtils.get_element(*DOM.Messages.input_message_area)
        msgArea.send_keys(p_msg)

    
    #
    # Just presses the 'send' button (assumes everything else is done).
    #
    def sendSMS(self):
        sendBtn = self.testUtils.get_element(*DOM.Messages.send_message_button)
        sendBtn.click()
        time.sleep(5)
        self.marionette.tap(sendBtn)
        
        time.sleep(1)
        self.parent.wait_for_element_not_present(*DOM.Messages.message_sending_spinner, timeout=120)
        
        # Go back to main messages screen
        header_back_button = self.testUtils.get_element(*DOM.Messages.header_back_button)
        self.testUtils.clickNTap(header_back_button)
       
    #
    # Wait for a new message.
    #
    def waitForNewSMS(self):
        self.parent.wait_for_element_displayed(*DOM.Messages.unread_message, timeout=180)

    #
    # Wait for new message (in the home screen).
    #
    def openNewSMS_homescreen(self):
        self.testUtils.goHome()
        self.testUtils.waitForNewStatusBarNew()
        return self.testUtils.openStatusBarNewNotif(DOM.Messages.statusbar_new_sms_url)
        
    #
    # Read last message.
    #
    def readLastSMSInThread(self):
        self.parent.wait_for_element_displayed(*DOM.Messages.received_messages)
        received_message = self.testUtils.get_elements(*DOM.Messages.received_messages)[-1]
        return str(received_message.text)

    #
    # Read and return the value of the new message.
    #
    def readNewSMS(self):
        self.parent.wait_for_element_displayed(*DOM.Messages.unread_message)
        unread_message = self.testUtils.get_element(*DOM.Messages.unread_message)
        self.marionette.tap(unread_message)

        # (From unit tests: "TODO Due to displayed bugs I cannot find a good wait for switch btw views")
        import time
        time.sleep(5)
        
        return self.readLastSMSInThread()

    #
    # Create and send a new SMS.
    #
    def createAndSendSMS(self, p_num, p_msg):
        #
        # Tap create new sms button.
        #
        self.parent.wait_for_element_displayed(*DOM.Messages.create_new_message_btn)
        newMsgBtn = self.testUtils.get_element(*DOM.Messages.create_new_message_btn)
        self.testUtils.clickNTap(newMsgBtn)
        
        #
        # Enter the number.
        #
        self.parent.wait_for_element_displayed(*DOM.Messages.target_number)
        numInput = self.testUtils.get_element(*DOM.Messages.target_number)
        numInput.send_keys(p_num)
        
        #
        # Enter the message.
        #
        self.enterSMSMsg(p_msg)
        
        #
        # Send the message.
        #
        self.sendSMS()
        

