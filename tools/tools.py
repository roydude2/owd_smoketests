import os
import base64
import time
import sys
from apps import DOM

class TestUtils():
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
        self.passed         = 0
        self.failed         = 0
    
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
            self.reportComment(iframe.get_attribute('src'))

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
    # Add an error to the error array.
    #
    def reportError(self, p_msg, p_fnam="X"):
        logMsg = p_msg
        
        if p_fnam != "X":
            logMsg = logMsg + " [screenshot = " + p_fnam + "]"
            
        self._failArray.append(logMsg)
    
    #
    # Add a comment to the results.
    #
    def reportComment(self, p_str):
        self._commentArray.append(p_str)

    #
    # Test that p_result is true.
    # The advantage to this over the standard 'assert's is that
    # this continues past a failure if p_stop is False.
    #
    def TEST(self, p_result, p_msg, p_stop = False):
        if not p_result:
            fnam = self.screenShotOnErr()
            self.reportError(p_msg, fnam)
            self.failed = self.failed + 1

            if p_stop:
                self.reportError("CANNOT CONTINUE PAST THIS ERROR - ABORTING THIS TEST!")
                sys.exit("Fatal error, quitting this test.")
        else:
            self.passed = self.passed + 1
        
    #
    # Test for a match between an element and a string
    # (found I was doing this rather a lot so it's better in a function).
    #
    def testMatch(self, p_el, p_type, p_val, p_name):
        if p_type == "value":
            test_str = str(p_el.get_attribute("value"))
        else:
            test_str = str(p_el.text)
            
        self.TEST( 
            (test_str == p_val), 
            "Expected " + p_name + " to be \"" + p_val + "\" but it was \"" + test_str + "\"" 
            )    

    #
    # Report results.
    #
    def reportResults(self):
        # Summary totals.
        print "==PASSED " + str(self.passed)
        print "==FAILED " + str(self.failed)
        # Deal with any assertion errors we came across.
        x = len(self._failArray)
        if x > 0:
            print "==RESULT FAIL!"
            for i in self._failArray:
                print "==ERROR " + i
        else:
            print "==RESULT All tests passed."
        
        # Display any comments.
        for i in self._commentArray:
            print "==COMMENT " + i
    
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
    # Return to the home screen.
    #
    def goHome(self):
        self.homescreen = self.parent.apps.launch('Homescreen')
        self.marionette.switch_to_frame()

    #
    # Displays the status / notification bar in the home screen.
    #
    def displayStatusBar(self):
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        
    #
    # Waits for a new notification in the status bar.
    #
    def waitForStatusBarNew(self):
        self.parent.wait_for_element_displayed(*DOM.GLOBAL.status_bar_new)        
        
    #
    # Clicks the first notification in the home status bar that matches
    # the passed in url.
    #
    def openStatusBarNewNotif(self, p_url):
        
        x = self.marionette.find_elements(*DOM.GLOBAL.status_bar_notifs)

        returnVar = False
        for i in x:
            if i.get_attribute("data-manifest-u-r-l") == p_url:
                returnVar = True
                self.marionette.tap(i)
        
        return returnVar
