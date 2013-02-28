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
    # Get a variable from the OS.
    #
    def get_os_variable(self, p_name, p_msg):
        return os.environ[p_name]
    
    #
    # Switch to frame (needed if accessing an app via another app, i.e.
    # launching Messages from Contacts).
    #
    def switchFrame(self, *p_frame):
        #
        # For some obscure reason you have to go 'home' before anywhere else.
        #
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
            self.reportComment("iFrame - " + iframe.get_attribute('src'))

    #
    # Connect to an iframe.
    #
    def connect_to_iframe(self, p_name):
        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
        for idx in range(0,iframes['length']):
            iframe = iframes[str(idx)]
            if p_name == iframe.get_attribute('src'):
                self.marionette.switch_to_frame(iframe)
                return True
        return False
        
    #
    # Wait for a statusbar setting to be displayed, then return to the
    # given frame.
    #
    def check_statusbar_for_icon(self, p_dom, p_returnFrame=""):
        self.marionette.switch_to_frame()
        x = self.marionette.find_element(*p_dom)
        isThere = x.is_displayed()
        
        if p_returnFrame != "":
            prev_frame = self.marionette.find_element(*p_returnFrame)
            self.marionette.switch_to_frame(prev_frame)
        
        return isThere
        
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
    # Quit this test suite.
    #
    def quitTest(self):
        self.reportError("CANNOT CONTINUE PAST THIS ERROR - ABORTING THIS TEST!")
        sys.exit("Fatal error, quitting this test.")

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
                self.quitTest()
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
    # Save the HTML of the current page to the specified file.
    #
    def savePageHTML(self, p_outfile):
        f = open(p_outfile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )

    #
    # Returns the header that matches a string.
    # NOTE: ALL headers in this frame are true for ".is_displayed()"!
    #
    def headerFound(self, p_str):
        headerName = self.get_elements(*DOM.GLOBAL.app_head)
        for i in headerName:
            if i.text == p_str:
                return True
                
        return False
        
    #
    # Scroll to next page (right).
    # Should change this to use marionette.flick() when it works.
    #
    def scrollHomescreenRight(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')
    
    #
    # Scroll around the homescreen until we find our app icon.
    #
    def findAppIcon(self, p_appName):
        self.homescreen = self.parent.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)        

        try:
            appIcon = self.marionette.find_element('css selector', DOM.GLOBAL.app_icon_css % p_appName)
            while not appIcon.is_displayed():
                self.scrollHomescreenRight()
                
            if appIcon.is_displayed():
                return appIcon
            else:
                return False
        except:
            return False
    
    #
    # Touch the home button (sometimes does something different to going home).
    #
    def touchHomeButton(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
    
    #
    # Return to the home screen.
    #
    def goHome(self):
        self.homescreen = self.parent.apps.launch('Homescreen')
        self.marionette.switch_to_frame()

    #
    # Activate edit mode in the homescreen.
    # ASSUMES YOU ARE ALREADY IN THE HOMESCREEN + CORRECT FRAME., i.e.
    #
    #    self.goHome()
    #    self.switchFrame(*DOM.GLOBAL.home_frame_locator)
    #
    # ... before you execute this!
    #
    def activateHomeEditMode(self):
        self.marionette.execute_script("window.wrappedJSObject.Homescreen.setMode('edit')")

    #
    # Return whether an app is present on the homescreen (i.e. 'installed').
    #
    def isAppInstalled(self, p_appName):
        self.homescreen = self.parent.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)

        x = ('css selector', DOM.GLOBAL.app_icon_css % p_appName)
        try:
            self.parent.wait_for_element_present(*x)
            return True
        except:
            return False

    #
    # Remove an app using the UI.
    #
    def uninstallApp(self, p_appName):
        #
        # Find the app icon.
        #
        myApp = self.findAppIcon("cool packaged app")
        self.TEST(myApp,
            "Could not find the app icon on the homescreen.", True)
        
        #
        # We found it! Go into edit mode (can't be done via marionette gestures yet).
        #
        self.activateHomeEditMode()
        
        #
        # Delete it.
        #
        delete_button = myApp.find_element(*DOM.GLOBAL.app_delete_icon)
        self.marionette.tap(delete_button)
        
        #
        # Confirm deletion.
        #
        self.parent.wait_for_element_displayed(*DOM.GLOBAL.app_confirm_delete)
        delete = self.marionette.find_element(*DOM.GLOBAL.app_confirm_delete)
        self.marionette.tap(delete)

        #
        # Once it's gone, go home and check the icon is no longer there.
        #
        self.touchHomeButton()
        self.TEST(not self.isAppInstalled(p_appName), "App is still installed after deletion.")



    #
    # Displays the status / notification bar in the home screen.
    #
    def displayStatusBar(self):
        #
        # The only reliable way I have to do this at the moment is via JS
        # (tapping it only worked sometimes).
        #
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        
    #
    # Waits for a new notification in the status bar (20s timeout by default).
    #
    def waitForStatusBarNew(self, p_dom=DOM.GLOBAL.status_bar_new, p_time=20):
        try: 
            self.parent.wait_for_element_present(*p_dom, timeout=p_time)
            return True
        except:
            return False

