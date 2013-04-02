from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    #################################################################################
    #
    # Methods which deal with reporting the results.
    #
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
        screenDump = self.screenShot(fnam)
        
        #
        # Dump the current page's html source too.
        #
        htmlDump = os.environ['RESULT_DIR'] + "/" + fnam + ".html"
        self.savePageHTML(htmlDump)
        return (htmlDump, screenDump)

    def viewAllIframes(self):
        #
        # DEV TOOL: this will loop through every iframe, report the "src", 
        # take a screenshot and capture the html.
        #
        # Because this is only meant as a dev aid (and shouldn't be in any released test
        # scripts), it reports to ERROR instead of COMMENT.
        #
        self.logResult("info", " ")
        self.logResult("info", "(FOR DEBUGGING:) All current iframes (screenshots + html source) ...")

        self.marionette.switch_to_frame()
        time.sleep(1)

        iframes = self.marionette.execute_script("return document.getElementsByTagName('iframe')")
        for idx in range(0,iframes['length']):
            self.marionette.switch_to_frame()
            iframe = iframes[str(idx)]
            iframe_src = iframe.get_attribute("src")
            iframe_x   = str(iframe.get_attribute("data-frame-origin"))
            self.marionette.switch_to_frame(iframe)
            time.sleep(1)

            log_msg = "iframe src=\"" + iframe_src + \
                      "\" data-frame-origin=\"" + iframe_x + "\""

            fnam = self.screenShotOnErr()

            self.logResult("info", " ")
            self.logResult("info", log_msg, fnam)
        

    def savePageHTML(self, p_outfile):
        #
        # Save the HTML of the current page to the specified file.
        #
        f = open(p_outfile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )


