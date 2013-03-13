import os
import base64
import time
import sys
import DOM
from gaiatest   import GaiaTestCase
from marionette import Marionette

class TestUtils(GaiaTestCase):
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent, p_testNum):
        self.parent         = p_parent
        self.apps           = p_parent.apps
        self.marionette     = p_parent.marionette
        self.testNum        = str(p_testNum)
        self._failArray     = []
        self._commentArray  = []
        self.errNum         = 0
        self.passed         = 0
        self.failed         = 0
        
        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        if True:
            self.marionette = p_parent.marionette
        
        #
        # Use this just for IDE autocomplete - you need to comment it out when
        # you've finished editing!
        #
#        self.marionette = Marionette()

        
    #
    # Get a variable from the OS.
    #
    def get_os_variable(self, p_name, p_msg):
        return os.environ[p_name]
    
    #
    # Get a DOM element - includes a check that the element is still
    # correct and stops the test if the element has changed.
    #
    # NOTE: Do not use this for:
    #        - Checking elements that are supposed to stop existing
    #          (i.e. wait_for_element_NOT_exists() )
    #        - Checking for frames.
    #        - Checking against elements which will be in a different frame to this one.
    #
    def verify(self, p_DOM_definition, p_timeOut=20):
        #
        # Split the variable into it's parts.
        #
        varname     = p_DOM_definition
        domElement  = eval(p_DOM_definition)
        
        try:
            self.wait_for_element_present(*domElement, timeout=p_timeOut)
        except:
            fileTag  = "DOM_error_screen"
            htmlFile = os.environ['RESULT_FILE'] + fileTag + ".html"
            shotFile = self.screenShot(fileTag)

            self.savePageHTML(htmlFile)
            

            errMsg    = "Element definition '" + p_DOM_definition + "' (\"" + domElement[0] + "\",\"" + domElement[1] + "\") "
            errMsg    = errMsg + "is invalid."
            self.reportError(errMsg)
            
            self.reportError("|__ [screenhtml = " + htmlFile + "]")
            self.reportError("|__", shotFile)
            
            self.quitTest()
        else:
            return domElement

#    #
#    # Switch to frame (needed if accessing an app via another app, i.e.
#    # launching Messages from Contacts).
#    #
#    def switchFrame(self, *p_frame):
#        #
#        # You have to go back to the top level before anywhere else.
#        #
#        self.marionette.switch_to_frame()
#
#        new_iframe = self.marionette.find_element(*p_frame)
#        self.marionette.switch_to_frame(new_iframe)
        
#    #
#    # Some iframes use id (such as facebook via contacts).
#    #
#    def connect_to_iframe_by_id(self, p_id):
#        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
#        for idx in range(0,iframes['length']):
#            iframe = iframes[str(idx)]
#            if p_id == iframe.get_attribute('id'):
#                self.marionette.switch_to_frame(iframe)
#                return True
#        return False

        
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
    # Also to help with the lack of docs just now - this will loop through every
    # iframe, report the "src", take a screenshot and capture the html in /tmp/royX.html.
    #
    # Because this is only meant as a dev aid (and shouldn't be in any released test
    # scripts), it reports to ERROR instead of COMMENT.
    #
    def viewAllIframes(self):
        self.marionette.switch_to_frame()
        time.sleep(1)
        y = 1
        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
        for idx in range(0,iframes['length']):
            self.marionette.switch_to_frame()
            iframe = iframes[str(idx)]
            self.reportError("Frame " + str(y) + " src=\"" + iframe.get_attribute("src") + "\", id=\"" + iframe.get_attribute("id") + "\"")
            self.marionette.switch_to_frame(iframe)
            time.sleep(1)
            self.savePageHTML("/tmp/roy" + str(y) + ".html")
            self.screenShot("DEBUG_" + str(y))
            y = y + 1
        
    def switchToFrame(self, p_tag, p_str, p_quitOnError=True):
        #
        # Switch to iframe based on the p_tag = p_string, i.e.
        # "id" = "my_iframe".
        #
        # Be aware that you USUALLY need to do this first:
        #
        #    "self.marionette.switch_to_frame()"
        #
        frameSpec = ("xpath", "//iframe[@" + p_tag + "='" + p_str + "']")
        
        try:
            self.wait_for_element_present(*frameSpec)
            iframe = self.marionette.find_element(*frameSpec)
            if self.marionette.switch_to_frame(iframe):
                return True    
        except:
            #
            # Ignore the exception - if we get pas this we've failed to switch.
            #
            pass
        
        if p_quitOnError:
            self.reportError("Could not switch to frame " + p_tag + "=\"" + p_str + "\".")
            self.quitTest()
        else:
            return False
    
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
            self.switchToFrame(*p_returnFrame)
        
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
        #
        # Build the error filename.
        #
        self.errNum = self.errNum + 1
        fnam = "_" + self.testNum + "_err_" + str(self.errNum)
        
        #
        # Record the screenshot.
        #
        x = self.screenShot(fnam)
        
        #
        # Dump the current page's html source too.
        #
        htmlDump = os.environ['RESULT_FILE'] + fnam + ".html"
        self.savePageHTML(htmlDump)
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
        self.screenShotOnErr()
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
    # formerly "testMatch"
    def checkMatch(self, p_el, p_type, p_val, p_name):
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
        self.wait_for_element_displayed(*p_element)
        el = self.marionette.find_element(*p_element)
        return el
        
    def get_elements(self, *p_elements):
        self.wait_for_element_displayed(*p_elements)
        els = self.marionette.find_elements(*p_elements)
        return els
    
    ##
    ## Quickly install an app.
    ##
    #def installAppQuick(self, p_name):
        ##
        ## The url address usually uses the name of the app, minus spaces
        ## and in lowercase.
        ##
        #appURL   = p_name.lower()
        #appURL   = appURL.replace(" ", "")
        #MANIFEST = "app://%s.gaiamobile.org/manifest.webapp" % appURL
        #self.marionette.switch_to_frame()
        #self.marionette.execute_script(
            #'navigator.mozApps.install("%s")' % MANIFEST)
    
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
        try:
            self.wait_for_element_present(*DOM.GLOBAL.app_head)
            headerName = self.marionette.find_elements(*DOM.GLOBAL.app_head)
            for i in headerName:
                if i.text == p_str:
                    return True
        except:
            return False
                
        return False
        
    #
    # Scroll to next page (right).
    # Should change this to use marionette.flick() when it works.
    #
    def scrollHomescreenRight(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')
    
    #
    # Scroll to previous page (left).
    # Should change this to use marionette.flick() when it works.
    #
    def scrollHomescreenLeft(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')
    
    #
    # Scroll around the homescreen until we find our app icon.
    #
    def findAppIcon(self, p_appName):
        self.apps.kill_all()
        self.homescreen = self.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)

        #
        # Bit long-winded, but it ensures the icon is displayed.
        #
        # We need to return the entire 'li' element, not just the
        # 'span' element (otherwise we can't use what's returned
        # to find the delete icon when the homescreen is in edit mode).
        #
        # As these dom specs are only ever useful right here, I'm not
        # defining them in DOM.
        #
        for i_page in range(1, 10):
            try:
                # (16 apps per page)
                for i_li in range(1,17):
                    try:
                        xpath_str = "//div[@class='page'][%s]//li[%s]" % (i_page, i_li)
                        x = self.marionette.find_element("xpath", 
                                                         xpath_str + "//span[text()='" + p_appName + "']")
                        
                        #
                        # Found it - return tihs list item!
                        #
                        myEl = self.marionette.find_element("xpath", xpath_str)
                        return myEl
                    except:
                        pass
            except:
                pass
            
            #
            # No such app in this page, try again.
            #
            self.scrollHomescreenRight()
            
        #
        # If we get here, we didn't find it!
        #
        return False
    
    #
    # Touch the home button (sometimes does something different to going home).
    #
    def touchHomeButton(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
    
    #
    # Long hold the home button to bring up the 'current running apps'.
    #
    def holdHomeButton(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('holdhome'));")
    
    #
    # Return to the home screen.
    #
    def goHome(self):
        self.apps.kill_all()
        self.homescreen = self.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)        

    #
    # Activate edit mode in the homescreen.
    # ASSUMES YOU ARE ALREADY IN THE HOMESCREEN + CORRECT FRAME., i.e.
    #
    #    self.goHome()
    #
    # ... before you execute this!
    #
    def activateHomeEditMode(self):
        self.marionette.execute_script("window.wrappedJSObject.Homescreen.setMode('edit')")

    #
    # Launch an app via the homescreen.
    #
    def launchAppViaHomescreen(self, p_name):
        if self.isAppInstalled(p_name):
            self.findAppIcon(p_name)
            time.sleep(1)
            x = ('css selector', DOM.GLOBAL.app_icon_css % p_name)
            myApp = self.marionette.find_element(*x)
            self.marionette.tap(myApp)
            return True
        else:
            return False
            
    #
    # Return whether an app is present on the homescreen (i.e. 'installed').
    #
    def isAppInstalled(self, p_appName):
        self.apps.kill_all()
        self.homescreen = self.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)

        x = ('css selector', DOM.GLOBAL.app_icon_css % p_appName)
        try:
            self.marionette.find_element(*x)
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
        myApp = self.findAppIcon(p_appName)
        self.TEST(myApp,
            "Could not find the app icon on the homescreen.", True)
        
        #
        # We found it! Go into edit mode (can't be done via marionette gestures yet).
        #
        self.activateHomeEditMode()
        
        #
        # Delete it (and refresh the 'myApp' object to include the new button).
        #
        # NOTE: This kind of 'element-within-an-element' isn't necessarily
        #       appropriate for 'verify'.
        #
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)
        myApp = self.findAppIcon(p_appName)
        
        #
        # If the app wasn't found, just return.
        #
        if not myApp: return False
        
        delete_button = myApp.find_element(*DOM.GLOBAL.app_delete_icon)
        self.marionette.tap(delete_button)
        
        #
        # Confirm deletion.
        #
        self.wait_for_element_displayed(*self.verify("DOM.GLOBAL.app_confirm_delete"))
        delete = self.marionette.find_element(*self.verify("DOM.GLOBAL.app_confirm_delete"))
        self.marionette.tap(delete)

        #
        # Once it's gone, go home and check the icon is no longer there.
        #
        self.touchHomeButton()
        self.TEST(not self.isAppInstalled(p_appName), "App is still installed after deletion.")
        
        return True

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
            self.wait_for_element_present(*p_dom, timeout=p_time)
            return True
        except:
            return False
