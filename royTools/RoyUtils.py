import os
import base64
import time
from royTools import DOMS

class testUtils():
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testNum):
        self._failArray     = []
        self._commentArray  = []
        self.marionette     = p_parentSelf.marionette
        self.parent         = p_parentSelf
        self.testNum        = str(p_testNum)
        self.errNum         = 0
    
    #
    # Switch to frame (needed if accessing an app via another app, i.e.
    # launching Messages from Contacts).
    #
    def switchFrame(self, *p_frame):
        self.marionette.switch_to_frame()
        sms_iframe = self.marionette.find_element(*p_frame)
        self.marionette.switch_to_frame(sms_iframe)
    #
    # Due to the lack of developer docs, this might help to provide a list
    # of current iframes.
    #
    def list_iframes(self):
        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
        for idx in range(0,iframes['length']):
            iframe = iframes[str(idx)]
            print iframe.get_attribute('src')

    #
    # Connect to an iframe.
    #
    def connect_to_iframe(self, p_name):
        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
        for idx in range(0,iframes['length']):
            iframe = iframes[str(idx)]
            if iframe.get_attribute('src') == p_name:
                self.marionette.switch_to_frame(iframe)
                return True
        
        
    
    #
    # Take a screenshot.
    #
    def screenShot(self, p_fileSuffix):
        outFile = os.environ['RESULT_FILE'] + p_fileSuffix + ".png"
        screenshot = self.marionette.screenshot()[22:] 
        with open(outFile, 'w') as f:
            f.write(base64.decodestring(screenshot))        
        return outFile

    #
    # Screenshot on error.
    #
    def screenShotOnErr(self):
        self.errNum = self.errNum + 1
        fnam = "_" + self.testNum + "_err_" + str(self.errNum)
        x = self.screenShot(fnam)
        return x
    
    #
    # Test for true.
    #
    def testTrue(self, p_result, p_msg):
        if not p_result:
            fnam = self.screenShotOnErr()
            self._failArray.append("--> " + p_msg + " [screenshot = " + fnam + "]")
        return
    
    #
    # Test for false.
    #
    def testFalse(self, p_result, p_msg):
        if p_result:
            fnam = self.screenShotOnErr()
            self._failArray.append("--> " + p_msg + " [screenshot = " + fnam + "]")
        return
    
    #
    # Test for a match between an element and a string.
    #
    def testMatch(self, p_el, p_type, p_val, p_name):
        if p_type == "value":
            test_str = str(p_el.get_attribute("value"))
        else:
            test_str = str(p_el.text)
            
        self.testTrue( 
            (test_str == p_val), 
            "Expected " + p_name + " to be \"" + p_val + "\" but it was \"" + test_str + "\"" 
            )    

    #
    # Add a comment to the results.
    #
    def reportComment(self, p_str):
        self._commentArray.append("**COMMENT: " + p_str)

    #
    # Report results.
    #
    def reportResults(self):
        # Deal with any assertion errors we came across.
        x = len(self._failArray)
        if x > 0:
            print "__RESULT FAIL!"
            for i in self._failArray:
                print "__" + i
        else:
            print "__RESULT All tests passed."
        
        # Display any comments.
        for i in self._commentArray:
            print "__" + i
    
    #
    # Wait for an element to be displayed, then return the element.
    #
    def get_element(self, *p_element):
        self.parent.wait_for_element_displayed(*p_element)
        el = self.marionette.find_element(*p_element)
        return el
        
    def get_elements(self, *p_elements):
        self.parent.wait_for_element_displayed(*p_elements)
        els = self.marionette.find_elements(*p_elements)
        return els
    
    #
    # Click (to highlight), then tap (to 'action') an element such as a
    # button or a link etc...
    #
    def clickNTap(self, p_element):
        p_element.click()
        self.marionette.tap(p_element)
        return
    
    #
    # Save the HTML of the current page to the specified file.
    #
    def savePageHTML(self, p_outfile):
        f = open(p_outfile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )

    #
    # Unlock the screen.
    #
    def unlockScreen(self):
        self.parent.lockscreen.unlock() # possibly not working!

        #lockscreen_element = self.marionette.find_element(*DOMS.Lockscreen.id)
        ##if lockscreen_element.is_displayed():
     
            #unlock_handle = self.marionette.find_element(*DOMS.Lockscreen.handle)
            #unlock_handle_x_centre = int(unlock_handle.size['width'] / 2)
            #unlock_handle_y_centre = int(unlock_handle.size['height'] / 2)

            ## Get the end position from the animation
            #lockscreen_area = self.marionette.find_element(*DOMS.Lockscreen.area)
            #end_animation_position = lockscreen_area.size['height'] - unlock_handle.size['height']

            ## Flick from unlock handle to (0, -end_animation_position) over 800ms duration
            #self.marionette.flick(unlock_handle, unlock_handle_x_centre, unlock_handle_y_centre, 0, 0 - end_animation_position, 800)

            ## Wait for the svg to animate and handle to disappear
            #self.wait_for_condition(lambda m: not unlock_handle.is_displayed())

            #unlock_button = self.marionette.find_element(*DOMS.unlock_button)
            #unlock_button.click()

            #lockscreen_element = self.marionette.find_element(*DOMS.Lockscreen.id)
            #self.wait_for_condition(lambda m: not lockscreen_element.is_displayed())

    #
    # Return to the home screen.
    #
    def goHome(self):
        self.homescreen = self.parent.apps.launch('Homescreen')
        self.marionette.switch_to_frame()

    #
    # Displays the status / notification bar in the home screen.
    #
    def displayStatusBar(self):
        statusBar = self.marionette.find_element(*DOMS.GLOBAL.status_bar)
        #self.marionette.tap(statusBar)
        statusBar.click()
        statusBar.click()
        
    #
    # Waits for a new notification in the status bar.
    #
    def waitForStatusBarNew(self):
        self.parent.wait_for_element_present(*DOMS.GLOBAL.status_bar_notifs)
        
        
    #
    # Clicks the first notification in the home status bar that matches
    # the passed in url.
    #
    def openStatusBarNewNotif(self, p_url):
        
        x = self.marionette.find_elements(*DOMS.GLOBAL.status_bar_notifs)

        returnVar = False
        for i in x:
            if i.get_attribute("data-manifest-u-r-l") == p_url:
                returnVar = True
                self.marionette.tap(i)
        
        return returnVar
