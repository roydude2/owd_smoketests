import os       , \
       base64   , \
       time     , \
       datetime , \
       sys      , \
       DOM
from gaiatest   import GaiaTestCase
from marionette import Marionette

class TestUtils(GaiaTestCase):
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.parent         = p_parent
        self.apps           = p_parent.apps
        self.marionette     = p_parent.marionette
        self._resultArray   = []
        self._commentArray  = []
        self.errNum         = 0
        self.passed         = 0
        self.failed         = 0
        self.start_time     = time.time()

        self.testNum        = self.get_os_variable("TEST_NUM")
        self.testDesc       = self.get_os_variable("TEST_DESC")
        self.det_fnam       = self.get_os_variable("DET_FILE")
        self.sum_fnam       = self.get_os_variable("SUM_FILE")
        
        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        if True:
            self.marionette = p_parent.marionette
        


    #################################################################################
    #
    # Methods which deal with reporting the results.
    #

    def logResult(self, p_result, p_msg, p_fnam=False):
        #
        # Add a test result to the result array.
        #
        logMsg = p_msg
        
        if p_fnam:
            logMsg = logMsg + " [screenshot = " + p_fnam + "]"
            
        #
        # The double brackets is intentional (add a 2 part
        # array: true/false + message).
        #
        self._resultArray.append((p_result, logMsg))
    
    def logComment(self, p_str):
        #
        # Add a comment to the comment array.
        #
        self._commentArray.append(p_str)

    def TEST(self, p_result, p_msg, p_stop = False):
        #
        # Test that p_result is true.
        #
        # The main advantage to this over the standard 'assert's is that
        # this continues past a failure if p_stop is False.
        # However, it also takes a screenshot and dumps the html source
        # if p_result is False.
        #
        fnam = False
        if not p_result:
            fnam = self.screenShotOnErr()
            self.failed = self.failed + 1
            self.logResult(p_result, p_msg, fnam)

            if p_stop:
                self.quitTest()
        else:
            self.passed = self.passed + 1
            self.logResult(p_result, p_msg)
        

    def reportResults(self):
        #
        # Create the final result file from the result and comment arrays
        # (run only once, at the end of each test case).
        #

        #
        # Create output files (summary, which is displayed and
        # details, which is not displayed).
        #
        test_time   = time.time() - self.start_time
        test_time   = round(test_time, 0)
        test_time   = str(datetime.timedelta(seconds=test_time))

        DET_FILE    = open(self.det_fnam, "w")
        SUM_FILE    = open(self.sum_fnam, "w")

        DET_FILE.write("Test case  : %s\n" % self.testNum)
        DET_FILE.write("Description: %s\n" % self.testDesc)
        DET_FILE.write("Time taken : %s\n" % str(test_time))

        boolStart = False
        for i in self._commentArray:
            if not boolStart:
                boolStart = True
                DET_FILE.write("Comments   : %s\n" % i)
            else:
                DET_FILE.write("           : %s\n" % i)

        x = len(self._resultArray)
        y = x
        res_str = "Passed"
        if x > 0:
            for i in self._resultArray:
                if not i[0]:
                    res_str = "FAILED <-- !"
                    y = y - 1
        
        totals = "(%d/%d)" %(y, x)
        SUM_FILE.write("[%s] %s %s: %s\n" % ( self.testNum.center(4), 
                                              self.testDesc.ljust(80), 
                                              totals.rjust(9),  
                                              res_str))
        
        DET_FILE.write("Passed     : %s\n" % str(self.passed))
        DET_FILE.write("Failed     : %s\n" % str(self.failed))
        DET_FILE.write("RESULT     : %s\n" % res_str)
        DET_FILE.write("\n")

        x = len(self._resultArray)
        boolFail = False
        if x > 0:
            for i in self._resultArray:
                if i[0]:
                    DET_FILE.write("   pass    - ")
                else:
                    DET_FILE.write("** FAIL ** - ")
                
                DET_FILE.write(i[1] + "\n")
        
        DET_FILE.close()
        SUM_FILE.close()



    #################################################################################
    #
    # Methods for general use.
    #

    def get_os_variable(self, p_name, p_msg=False):
        #
        # Get a variable from the OS.
        #
        if p_name == "ENTER":
            return ""
        else:
            return os.environ[p_name]
    
    def verify(self, p_DOM_definition, p_timeOut=20):
        #
        # Return a DOM element - includes a check that the element is still
        # correct and stops the test if the element has changed.
        #
        # NOTE: Do not use this for:
        #        - Elements that are supposed to stop existing
        #          (i.e. wait_for_element_not_exists() )
        #        - Frames.
        #        - Elements which will be in a different frame to this one.
        #

        #
        # Split the variable into it's parts.
        #
        varname     = p_DOM_definition
        
        try:
            domElement  = eval(p_DOM_definition)
        except:
            #
            # Since this isn't really a test of the app (more of a test of our
            # definitions), I'm not reporting this as a pass / fail 'TEST' unless
            # it fails.
            #
            self.logResult(False, 
                           "'" + p_DOM_definition + "' is not found in the DOM files.")
            self.quitTest()
        
        try:
            self.wait_for_element_present(*domElement, timeout=p_timeOut)
        except:
            fileTag  = "DOM_error_screen"
            htmlFile = os.environ['RESULT_DIR'] + "/" + fileTag + ".html"
            shotFile = self.screenShot(fileTag)

            self.savePageHTML(htmlFile)
            

            errMsg    = "Element definition '" + p_DOM_definition + "' (\"" + domElement[0] + "\",\"" + domElement[1] + "\") "
            errMsg    = errMsg + "is invalid."
            self.logResult(False, errMsg)
            
            self.logResult(False, "|__ [screenhtml = " + htmlFile + "]")
            self.logResult(False, "|__", shotFile)
            
            self.quitTest()
        else:
            return domElement

    def viewAllIframes(self):
        #
        # DEV TOOL: this will loop through every iframe, report the "src", 
        # take a screenshot and capture the html in /tmp/royX.html.
        #
        # Because this is only meant as a dev aid (and shouldn't be in any released test
        # scripts), it reports to ERROR instead of COMMENT.
        #
        self.marionette.switch_to_frame()
        time.sleep(1)
        y = 1
        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
        for idx in range(0,iframes['length']):
            self.marionette.switch_to_frame()
            iframe = iframes[str(idx)]
            iframe_src = iframe.get_attribute("src")
            iframe_id  = iframe.get_attribute("id")
            iframe_x   = str(iframe.get_attribute("data-frame-origin"))
            self.marionette.switch_to_frame(iframe)
            time.sleep(1)

            self.logResult(False, 
                           "Frame " + str(y) + \
                           " src=\"" + iframe_src + \
                           "\" x=\"" + iframe_x + \
                           "\", id=\"" + iframe_id + "\"")
            self.savePageHTML("/tmp/roy" + str(y) + ".html")
            self.screenShot("DEBUG_" + str(y))

            y = y + 1
        
    def switchToFrame(self, p_tag, p_str, p_quitOnError=True):
        #
        # Switch to a different iframe based on tag and value.
        # NOTE: You *may* need to use self.marionette.switch_to_frame() first!
        #
        time.sleep(1)
        x = self.marionette.find_elements("tag name", "iframe")
        for i in x:
            if i.get_attribute(p_tag) == p_str:
                self.marionette.switch_to_frame(i)
                return True
        
        if p_quitOnError:
            self.logResult(False, "Switch to frame " + p_tag + "=\"" + p_str + "\".")
            self.quitTest()
        else:
            return False
    
    def check_statusbar_for_icon(self, p_dom, p_returnFrame=False):
        #
        # Wait for a statusbar setting to be displayed, then return to the
        # given frame (doesn't wait, just expects it to be there).
        #
        self.marionette.switch_to_frame()
        x = self.marionette.find_element(*p_dom)
        isThere = x.is_displayed()
        
        if p_returnFrame:
            self.switchToFrame(*p_returnFrame)
        
        return isThere
        
    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = os.environ['RESULT_DIR'] + "/" + p_fileSuffix + ".png"
        screenshot = self.marionette.screenshot()[22:] 
        with open(outFile, 'w') as f:
            f.write(base64.decodestring(screenshot))        
        return outFile

    def screenShotOnErr(self):
        #
        # Take a screenshot on error (increments the file number).
        #

        #
        # Build the error filename.
        #
        self.errNum = self.errNum + 1
        fnam = self.testNum + "_err_" + str(self.errNum)
        
        #
        # Record the screenshot.
        #
        x = self.screenShot(fnam)
        
        #
        # Dump the current page's html source too.
        #
        htmlDump = os.environ['RESULT_DIR'] + "/" + fnam + ".html"
        self.savePageHTML(htmlDump)
        return x

    def quitTest(self, p_msg=False):
        #
        # Quit this test suite.
        #
        self.screenShotOnErr()
        if not p_msg:
            msg = "CANNOT CONTINUE PAST THIS ERROR - ABORTING THIS TEST!"
        else:
            msg = p_msg

        self.logResult(False, msg)
        sys.exit(0) #"Fatal error, quitting this test.")
        
    def waitForNotDisplayed(self, p_timeout, p_msg, p_stop, p_element):
        #
        # Waits for an element to be displayed and captures the error if not.
        #
        boolOK = True
        try:
            self.wait_for_element_not_displayed(*p_element, timeout=p_timeout)
        except:
            boolOK = False
            
        self.TEST(boolOK, p_msg, p_stop)
        
        return boolOK
        
    def waitForDisplayed(self, p_timeout, p_msg, p_stop, p_element):
        #
        # Waits for an element to be displayed and captures the error if not.
        #
        boolOK = True
        try:
            self.wait_for_element_displayed(*p_element, timeout=p_timeout)
        except:
            boolOK = False
            
        self.TEST(boolOK, p_msg, p_stop)
        
        return boolOK
        
    def get_element(self, *p_element):
        #
        # Wait for an element to be displayed, then return the element
        # (or False).
        #
        boolOK = True
        try:
            self.wait_for_element_displayed(*p_element)
            el = self.marionette.find_element(*p_element)
        except:
            boolOK = False
        
        self.TEST(boolOK, 
                       "Element (\"" + \
                       p_element[0] + "\", \"" + \
                       p_element[1] + "\") is displayed before timeout.")
        if boolOK:
            return el
        else:
            return False
        
    def get_elements(self, *p_elements):
        #
        # Wait for an element to be displayed, then return the element
        # (or False).
        #
        boolOK = True
        try:
            self.wait_for_element_displayed(*p_elements)
            el = self.marionette.find_elements(*p_elements)
        except:
            boolOK = False
        
        self.TEST(boolOK, 
                       "Elements (\"" + \
                       p_elements[0] + "\", \"" + \
                       p_elements[1] + "\") is displayed before timeout.")
        if boolOK:
            return el
        else:
            return False
    
    ##
    ## Quickly install an app. - CURRENTLY NEEDS MORE INFO THAN  HAVE.
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
    
    def savePageHTML(self, p_outfile):
        #
        # Save the HTML of the current page to the specified file.
        #
        f = open(p_outfile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )

    def headerCheck(self, p_str):
        #
        # Returns the header that matches a string.
        # NOTE: ALL headers in this iframe return true for ".is_displayed()"!
        #
        boolOK = False
        try:
            self.wait_for_element_present(*DOM.GLOBAL.app_head)
            headerName = self.marionette.find_elements(*DOM.GLOBAL.app_head)
            for i in headerName:
                if i.text == p_str:
                    if i.is_displayed():
                        boolOK = True
                        break
        except:
            boolOK = False
                
        self.TEST(boolOK, "Header \"" + p_str + "\" is found.")
        return boolOK
        
    def setTimeToNow(self):
        #
        # Set the phone's time (using gaia data_layer instead of the UI).
        #
        self.parent.data_layer.set_time(time.time() * 1000)
        
    def scrollHomescreenRight(self):
        #
        # Scroll to next page (right).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')
    
    def scrollHomescreenLeft(self):
        #
        # Scroll to previous page (left).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')
    
    def findAppIcon(self, p_appName, p_reloadHome=True):
        #
        # Scroll around the homescreen until we find our app icon.
        #
        if p_reloadHome:
            #
            # If this doesn't happen, it is assumed you are already
            # in the correct iframe.
            #
            self.goHome()

        #
        # Bit long-winded, but it ensures the icon is displayed.
        #
        # We need to return the entire 'li' element, not just the
        # 'span' element (otherwise we can't use what's returned
        # to find the delete icon when the homescreen is in edit mode).
        #
        # As these dom specs are only ever going to be useful here, 
        # I'm not defining them in DOM.
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
            # No such app in this page, try again (only scroll of we reloaded the home page).
            #
            if p_reloadHome: self.scrollHomescreenRight()
                
        #
        # If we get here, we didn't find it!
        #
        return False
    
    def touchHomeButton(self):
        #
        # Touch the home button (sometimes does something different to going home).
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
    
    def holdHomeButton(self):
        #
        # Long hold the home button to bring up the 'current running apps'.
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('holdhome'));")
    
    def goHome(self):
        #
        # Return to the home screen.
        #
        self.apps.kill_all()
#        self.homescreen = self.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
#        self.marionette.switch_to_frame(self.homescreen.frame)
        self.switchToFrame(*DOM.GLOBAL.homescreen_iframe)
        time.sleep(1)

    def activateHomeEditMode(self):
        #
        # Activate edit mode in the homescreen.
        # ASSUMES YOU ARE ALREADY IN THE HOMESCREEN + CORRECT FRAME., i.e.
        #
        #    self.goHome()
        #
        # ... before you execute this!
        #
        self.marionette.execute_script("window.wrappedJSObject.Homescreen.setMode('edit')")

    def launchAppViaHomescreen(self, p_name):
        #
        # Launch an app via the homescreen.
        #
        boolOK = False
        if self.findAppIcon(p_name):
            time.sleep(1)
            x = ('css selector', DOM.GLOBAL.app_icon_css % p_name)
            myApp = self.marionette.find_element(*x)
            self.marionette.tap(myApp)
            boolOK = True
        else:
            boolOK = False
        
        return boolOK
            
    def isAppInstalled(self, p_appName):
        #
        # Return whether an app is present on the homescreen (i.e. 'installed').
        #
        self.marionette.switch_to_frame()
        self.switchToFrame(*DOM.GLOBAL.homescreen_iframe)

        x = ('css selector', DOM.GLOBAL.app_icon_css % p_appName)
        try:
            self.marionette.find_element(*x)
            return True
        except:
            return False

    def uninstallApp(self, p_appName):
        #
        # Remove an app using the UI.
        #

        #
        # Verify that the app is installed.
        #
        if not self.isAppInstalled(p_appName):
            return False
        
        #
        # Find the app icon.
        #
        myApp = self.findAppIcon(p_appName)
        
        #
        # We found it! Go into edit mode (can't be done via marionette gestures yet).
        #
        self.activateHomeEditMode()
        
        #
        # Delete it (and refresh the 'myApp' object to include the new button).
        #
        # NOTE: This kind of 'element-within-an-element' isn't necessarily
        #       appropriate for 'verify', so don't.
        #
        myApp = self.findAppIcon(p_appName, False)
        
        delete_button = myApp.find_element(*DOM.GLOBAL.app_delete_icon)
        
        if not delete_button: return False
        
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
        time.sleep(2)
        self.touchHomeButton()
        self.touchHomeButton()
        self.TEST(not self.isAppInstalled(p_appName), "App is still installed after deletion.")
        
        return True

    def displayStatusBar(self):
        #
        # Displays the status / notification bar in the home screen.
        #
        # The only reliable way I have to do this at the moment is via JS
        # (tapping it only worked sometimes).
        #
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        
    def waitForStatusBarNew(self, p_dom=DOM.GLOBAL.status_bar_new, p_time=20):
        #
        # Waits for a new notification in the status bar (20s timeout by default).
        #
        try: 
            self.wait_for_element_present(*p_dom, timeout=p_time)
            return True
        except:
            return False
