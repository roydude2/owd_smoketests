import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppMarket(GaiaTestCase):
    
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
        self.app = self.apps.launch('Marketplace')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)
        
    def searchForApp(self, p_app):
        #
        # Search for an app in the market.
        #
        from marionette.keys import Keys

        search_field = ("id", "search-q")
        
        #
        # Scroll a little to make the search area visible.
        #
        self.marionette.execute_script('window.scrollTo(0, 10)')        
        
        x = self.marionette.find_element(*search_field)
        x.send_keys(p_app)
        x.send_keys(Keys.RETURN)

    def selectSearchResultApp(self, p_app, p_author):
        #
        # Select the application we want from the list returned by
        # self.searchForApp().
        #
        self._search_results_area_locator = ('id', 'search-results')
        self._search_result_locator = ('css selector', '#search-results li.item')
        self._app_name_locator = ('xpath', '//h3')
        self._author_locator = ('css selector', '.author.lineclamp.vital')
        
        self.wait_for_element_displayed(*self._search_results_area_locator)
        results = self.marionette.find_elements(*self._search_result_locator)
        
        if len(results) <= 0:
            return False
        
        for app in results:
            if  app.find_element(*self._app_name_locator).text == p_app and \
                app.find_element(*self._author_locator).text == p_author:
                self.marionette.tap(app)
                return True
            
        return False


    #
    # Install an app.
    #
    def install_app(self, p_app, p_author):
        self.searchForApp(p_app)
        
        if not self.selectSearchResultApp(p_app, p_author):
            self.UTILS.reportError("App '" + p_app + "' with author '" + \
                                   p_author + "' not found in the market.")
            return False
        
        #
        # Click to install the app.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.app_details_header"))
        self.UTILS.TEST(x.text == p_app, "Expected title in app details to be '" + p_app + "', but was '" + x.text + "'.")
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.install_button"))
        self.marionette.tap(x)

        #
        # Confirm the installation of the app.
        #
        self.marionette.switch_to_frame()

        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Market.confirm_install_button"))
        yes_button = self.marionette.find_element(*self.UTILS.verify("DOM.Market.confirm_install_button"))
        self.marionette.tap(yes_button)
        self.wait_for_element_not_displayed(*DOM.Market.confirm_install_button)
        
        return True

    #
    # Check the app is installed as an icon in the home screen (probably need to swipe right
    # to actually see it physically).
    #
    def verify_app_installed(self, p_app):            
        #
        # Go back to the home page and check the app is installed.
        #
        self.UTILS.TEST(self.UTILS.isAppInstalled(p_app), "App icon not found in homescreen.")
        
        
    
