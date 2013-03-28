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
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS

    def launchMe(self):
        #
        # Sometimes the market doesn't load 1st time (just when automated
        # for some reason). So check and try again if necessary.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Marketplace')
        self.UTILS.waitForNotDisplayed(20, "Loading overlay stops being displayed", False, DOM.GLOBAL.loading_overlay);

    def launch(self):
        self.launchMe()
        
        try:
            self.wait_for_element_present(*DOM.Market.search_query)
        except:
            self.launchMe()
            
        
    def searchForApp(self, p_app):
        #
        # Search for an app in the market.
        #
        from marionette.keys import Keys

        #
        # Scroll a little to make the search area visible.
        #
        self.marionette.execute_script('window.scrollTo(0, 10)')        
        
        x = self.marionette.find_element(*self.UTILS.verify("DOM.Market.search_query"))
        x.send_keys(p_app)
        x.send_keys(Keys.RETURN)

    def selectSearchResultApp(self, p_app, p_author):
        #
        # Select the application we want from the list returned by
        # self.searchForApp().
        #
        self.UTILS.waitForDisplayed(20, "Search results displayed.", True, DOM.Market.search_results_area)
        results = self.UTILS.get_elements(*DOM.Market.search_results)
        
        if len(results) <= 0:
            return False
        
        for app in results:
            if  app.find_element(*DOM.Market.app_name).text == p_app and \
                app.find_element(*DOM.Market.author).text == p_author:
                self.marionette.tap(app)
                return True
            
        return False


    def install_app(self, p_app, p_author):
        #
        # Install an app.
        #
        self.searchForApp(p_app)
        
        if not self.selectSearchResultApp(p_app, p_author):
            self.UTILS.logResult(False, "App '" + p_app + "' with author '" + \
                                   p_author + "' is found in the market.")
            return False
        
        #
        # Click to install the app.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.app_details_header"))
        self.UTILS.TEST(x.text == p_app, "Title in app details matches '" + p_app + "' (it was '" + x.text + "').")
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.install_button"))
        
        # Sometimes this needs to be clicked ... sometimes tapped ... just do 'everything'!
        x.click()
        self.marionette.tap(x)

        #
        # Confirm the installation of the app.
        #
        self.marionette.switch_to_frame()

        yes_button = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.confirm_install_button"))
        self.marionette.tap(yes_button)

#        self.wait_for_element_not_displayed(*DOM.Market.confirm_install_button)
        self.UTILS.waitForNotDisplayed(20, "Confirm install button stops being displayed", False, DOM.Market.confirm_install_button);
        
        return True

        
        
    
