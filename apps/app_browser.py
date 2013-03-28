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
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS

    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Browser')
        self.UTILS.waitForNotDisplayed(20, "Loading overlay stops being displayed", False, DOM.GLOBAL.loading_overlay);

    def is_throbber_visible(self):
        #
        # Just checks that the animated wait icon is still present.
        #
        return self.marionette.find_element(*self.UTILS.verify("DOM.Browser.throbber")).get_attribute('class') == 'loading'
    
    def open_url(self, p_url):
        #
        # Open url.
        #
        x=self.UTILS.get_element(*self.UTILS.verify("DOM.Browser.url_input"))
        self.UTILS.logComment("Using URL " + p_url)
        x.send_keys(p_url)
        
        x=self.UTILS.get_element(*self.UTILS.verify("DOM.Browser.url_go_button"))
        self.marionette.tap(x)
        
        #
        # Wait for throbber to appear then dissappear.
        #
        self.UTILS.waitForDisplayed(20, "Browser 'throbber' appears while loading a url.", True, DOM.Browser.throbber)
#        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Browser.throbber"))
        self.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=120)
    
        self.UTILS.TEST(self.check_page_loaded(p_url), "Web page loaded correctly.")
    
    def check_page_loaded(self, p_url):
        #
        # Check the page didn't have a problem.
        #

        #
        # Switch to the browser content frame and check the contents.
        #
        # The "src" will have the protocol on the front, such as "http://" or "https://" or whatever.
        # It could also expand to have more on the end of the url, which basically makes it a bit
        # unpredictable, so I'm using the class name.
        # However, if you decide to use it in the future, here's how:
#        iframe_dom = ("xpath", "//iframe[contains(@src,'%s')]" % p_url)
#        ... do the 'wait_for_element...' part. If that passes:
#        x = self.marionette.find_element(*iframe_dom)
#        self.UTILS.switchToFrame("src", x.get_attribute("src"))        iframe_dom = ("class name", "browser-tab")

        self.UTILS.switchToFrame(*DOM.Browser.website_frame)

        try:
            x = self.marionette.find_element(*DOM.Browser.page_problem)
            if x.is_displayed():
                return False
        except:
            return True
