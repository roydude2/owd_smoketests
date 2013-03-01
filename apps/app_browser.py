from apps import DOM
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.UTILS  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.parent.apps.kill_all()
        self.app = self.parent.apps.launch('Browser')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    #
    # Open url.
    #
    def open_url(self, p_url):
        x=self.UTILS.get_element(*DOM.Browser.url_input)
        self.UTILS.reportComment("Using URL " + p_url)
        x.send_keys(p_url)
        
        x=self.UTILS.get_element(*DOM.Browser.url_go_button)
        self.marionette.tap(x)
        
        #
        # Wait for throbber to appear then dissappear.
        #
        self.parent.wait_for_element_displayed(*DOM.Browser.throbber)
        self.parent.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=120)
    
    def is_throbber_visible(self):
        return self.marionette.find_element(*DOM.Browser.throbber).get_attribute('class') == 'loading'
    
    
    #
    # Check the page didn't have a problem.
    #
    def check_page_loaded(self):
        x=self.UTILS.get_element(*DOM.Browser.url_input)
        testStr = x.get_attribute("value")
        
        #
        # Switch to the browser content frame (so a snapshot on error will show the browser
        # contents).
        #
        browser_frame = self.marionette.find_element(*DOM.Browser.browser_page_frame)
        self.marionette.switch_to_frame(browser_frame)

        self.UTILS.TEST("Problem loading page" != testStr, "Had a problem loading the page.")
