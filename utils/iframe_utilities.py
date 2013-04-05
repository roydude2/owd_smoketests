from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
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
            iframe = iframes[str(idx)]
            iframe_src = iframe.get_attribute("src")
            iframe_x   = str(iframe.get_attribute("data-frame-origin"))
            self.marionette.switch_to_frame()
            self.marionette.switch_to_frame(iframe)
            time.sleep(1)

            log_msg = "iframe src=\"" + iframe_src + \
                      "\" data-frame-origin=\"" + iframe_x + "\""

            fnam = self.screenShotOnErr()

            self.logResult("info", " ")
            self.logResult("info", log_msg, fnam)
        
