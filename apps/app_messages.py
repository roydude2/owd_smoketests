import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppMessages(GaiaTestCase):
    
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
        self.app = self.apps.launch('Messages')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    #
    # Create and send a message (assumes we are in a new 'create new message'
    # screen with the destination number filled in already).
    #
    def enterSMSMsg(self, p_msg):
        msgArea = self.UTILS.get_element(*self.UTILS.verify("DOM.Messages.input_message_area"))
        msgArea.send_keys(p_msg)

    
    #
    # Just presses the 'send' button (assumes everything else is done).
    #
    def sendSMS(self):
        sendBtn = self.UTILS.get_element(*self.UTILS.verify("DOM.Messages.send_message_button"))
        sendBtn.click()
        time.sleep(5)
        self.marionette.tap(sendBtn)
        
        time.sleep(1)
        self.wait_for_element_not_present(*DOM.Messages.message_sending_spinner, timeout=120)
        
        # Go back to main messages screen
        header_back_button = self.UTILS.get_element(*self.UTILS.verify("DOM.Messages.header_back_button"))
        self.marionette.tap(header_back_button)
    
    #
    # Get the element of the new SMS from the status bar notification.
    #
    def waitForSMSNotifier(self, p_num, p_timeout):
        #
        # Now switch to the 'home' frame to watch for the status bar notification
        # (just to be sure we're in the correct frame!).
        #
        self.marionette.switch_to_frame()
        
        #
        # Bit complicated - first we need to create the string to wait for.
        #
        x=( DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1] % p_num)
        
        #
        # Wait for the notification to be present for this number 
        # in the popup messages (this way we make sure it's coming from our number,
        # as opposed to just containing our number in the notification).
        #
        x = self.UTILS.waitForStatusBarNew(x, p_timeout)
        
        if not x:
            self.UTILS.reportError("Failed to locate new sms before timeout!")
            errmsg = "(NOTE: If you asked the device to message itself, the return message may have just returned "
            errmsg = errmsg + "too quickly to be detected - try using the number of a different device.)"
            self.UTILS.reportError(errmsg)
            return False
        else:
            return True
    
    #
    # Click new sms in the home page status bar notificaiton.
    #
    def clickSMSNotifier(self, p_num):
        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        
        #
        # The popup vanishes too quickly to be reliably clicked, so we
        # need to loop through the elements in the drop down notif bar
        # and click the relevant link there instead.
        #
        self.UTILS.displayStatusBar()

        x = self.marionette.find_elements(*self.UTILS.verify("DOM.GLOBAL.status_bar_count"))
        
        for i in range(0, len(x)):
            #
            # Very tricky - the 'tappable' part is actually the parent div :(
            #
            #   elParent: this is what has to be clicked to 'action' sms app.
            #   elChild : this is where the number is stored (so match on this).
            #
            # (there MUST be an easier way to do this - took me hours
            #  of trial-and-error to figure it out! ;[ )
            #
            elParent = DOM.Messages.statusbar_all_notifs % (i+1)
            elChild  = DOM.Messages.statusbar_all_notifs % (i+1) + "/div[1]"
            
            elC = self.marionette.find_element('xpath', elChild)

            if p_num in elC.text:
                #
                # Match - get the parent div and click it.
                # 
                elP = self.marionette.find_element('xpath', elParent)
                self.marionette.tap(elP)
                break

        #
        # Switch back to the messaging app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        

    #
    # Read last message.
    #
    def readLastSMSInThread(self):
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Messages.received_messages"))
        received_message = self.UTILS.get_elements(*self.UTILS.verify("DOM.Messages.received_messages"))[-1]
        return str(received_message.text)

    #
    # Read and return the value of the new message received from number.
    #
    def readNewSMS(self, p_FromNum):
        x = self.marionette.find_element("xpath", DOM.Messages.messages_from_num % p_FromNum)

        self.marionette.tap(x)
        
        # (From gaiatest: "TODO Due to displayed bugs I cannot find a good wait for switch btw views")
        time.sleep(5)
        
        #
        # Return the last comment in this thread.
        #
        return self.readLastSMSInThread()

    #
    # Create and send a new SMS.
    #
    def createAndSendSMS(self, p_num, p_msg):
        #
        # Tap create new sms button.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Messages.create_new_message_btn"))
        newMsgBtn = self.UTILS.get_element(*self.UTILS.verify("DOM.Messages.create_new_message_btn"))
        self.marionette.tap(newMsgBtn)
        
        #
        # Enter the number.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Messages.target_number"))
        numInput = self.UTILS.get_element(*self.UTILS.verify("DOM.Messages.target_number"))
        numInput.send_keys(p_num)
        
        #
        # Enter the message.
        #
        self.enterSMSMsg(p_msg)
        
        #
        # Send the message.
        #
        self.sendSMS()
        

