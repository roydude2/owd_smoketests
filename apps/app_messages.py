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
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS



    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Messages')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay", False);

    def enterSMSMsg(self, p_msg):
        #
        # Create and send a message (assumes we are in a new 'create new message'
        # screen with the destination number filled in already).
        #
        msgArea = self.UTILS.getElement(DOM.Messages.input_message_area, "Input message area")
        msgArea.send_keys(p_msg)

    
    def sendSMS(self):
        #
        # Just presses the 'send' button (assumes everything else is done).
        #
        sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.click()
        time.sleep(5)
        self.marionette.tap(sendBtn)
        
        time.sleep(1)
        self.UTILS.waitForNotElements(DOM.Messages.message_sending_spinner, "'Sending' icon", True, 120)
        
        # Go back to main messages screen
        header_back_button = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        self.marionette.tap(header_back_button)
    
    def waitForSMSNotifier(self, p_num, p_timeout):
        #
        # Get the element of the new SMS from the status bar notification.
        #

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
            self.UTILS.logResult(False, "New SMS is received.")
            errmsg = "(NOTE: If you asked the device to message itself, the return message will return "
            errmsg = errmsg + "too quickly to be detected - try using the number of a different device.)"
            self.UTILS.logResult(False, errmsg)
            return False
        else:
            return True
    
    def clickSMSNotifier(self, p_num):
        #
        # Click new sms in the home page status bar notificaiton.
        #

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

        x = self.UTILS.getElements(DOM.Messages.statusbar_all_notifs, "Statusbar notifications")
        
        for elP in x:
            #
            # Bit tricky - the 'tappable' part is actually the parent "div".
            #
            #   elP: this is what has to be clicked to 'action' sms app.
            #   elC: this is where the number is stored (so match on this).
            #
            elC      = elP.find_elements("xpath", "//div")
            
            for ic in elC:
                if p_num in ic.text:
                    self.marionette.tap(elP)
                    break
            
        #
        # Switch back to the messaging app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        

    def readLastSMSInThread(self):
        #
        # Read last message "[-1]" gives us the last element in an array.
        #
#        self.wait_for_element_displayed(DOM.Messages.received_messages)

        received_message = self.UTILS.getElements(DOM.Messages.received_messages, "Received messages")[-1]
        return str(received_message.text)

    def readNewSMS(self, p_FromNum):
        #
        # Read and return the value of the new message received from number.
        #
        x = self.UTILS.getElement(("xpath", DOM.Messages.messages_from_num % p_FromNum), "Message from '" + p_FromNum + "'")
        self.marionette.tap(x)
        
        # (From gaiatest: "TODO Due to displayed bugs I cannot find a good wait for switch btw views")
        time.sleep(5)
        
        #
        # Return the last comment in this thread.
        #
        return self.readLastSMSInThread()

    def createAndSendSMS(self, p_num, p_msg):
        #
        # Create and send a new SMS.
        #

        #
        # Tap create new sms button.
        #
        newMsgBtn = self.UTILS.getElement(DOM.Messages.create_new_message_btn, "Create new message button")
        self.marionette.tap(newMsgBtn)
        
        #
        # Enter the number.
        #
        numInput = self.UTILS.getElement(DOM.Messages.target_number, "Target number field")
        numInput.send_keys(p_num)
        
        #
        # Enter the message.
        #
        self.enterSMSMsg(p_msg)
        
        #
        # Send the message.
        #
        self.sendSMS()
        

