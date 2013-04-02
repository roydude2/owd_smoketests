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
    
