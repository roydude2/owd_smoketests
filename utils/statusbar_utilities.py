from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    def isIconInStatusBar(self, p_dom, p_returnFrame=False):
        #
        # Check an icon is in the statusbar, then return to the
        # given frame (doesn't wait, just expects it to be there).
        #
        self.marionette.switch_to_frame()
        x = self.marionette.find_element(*p_dom)
        isThere = x.is_displayed()
        
        if p_returnFrame:
            self.switchToFrame(*p_returnFrame)
        
        return isThere
        
    def displayStatusBar(self):
        #
        # Displays the status / notification bar in the home screen.
        #
        # The only reliable way I have to do this at the moment is via JS
        # (tapping it only worked sometimes).
        #
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        
    def waitForStatusBarNew(self, p_dom=DOM.Statusbar.status_bar_new, p_time=20):
        #
        # Waits for a new notification in the status bar (20s timeout by default).
        #
        try: 
            self.wait_for_element_present(*p_dom, timeout=p_time)
            return True
        except:
            return False
