import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppBrowser(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self, 00)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS



    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Browser')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    #
    # Open url.
    #
    def open_url(self, p_url):
        x=self.UTILS.get_element(*self.UTILS.verify("DOM.Browser.url_input"))
        self.UTILS.reportComment("Using URL " + p_url)
        x.send_keys(p_url)
        
        x=self.UTILS.get_element(*self.UTILS.verify("DOM.Browser.url_go_button"))
        self.marionette.tap(x)
        
        #
        # Wait for throbber to appear then dissappear.
        #
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Browser.throbber"))
        self.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=120)
    
    def is_throbber_visible(self):
        return self.marionette.find_element(*self.UTILS.verify("DOM.Browser.throbber")).get_attribute('class') == 'loading'
    
    
    #
    # Check the page didn't have a problem.
    #
    def check_page_loaded(self):
        #
        # Switch to the browser content frame (so a snapshot on error will show the browser
        # contents).
        #
        self.UTILS.switchToFrame("mozbrowser", "")
#        browser_frame = self.marionette.find_element(*self.UTILS.verify("DOM.Browser.browser_page_frame"))
#        self.marionette.switch_to_frame(browser_frame)

        boolOK = True
        try:
            x = self.marionette.find_element("xpath", "//*[text()='Problem loading page']")
            if x.is_displayed():
                boolOK = False
        except:
            boolOK = True
        
        self.UTILS.TEST(boolOK, "Had a problem loading the page.")
