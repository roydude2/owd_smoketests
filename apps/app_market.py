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

    #
    # Install an app.
    #
    def install_app(self, p_app):
        #
        # Because of the change to the search (and the fact that I can't get Marionette 'flick()' to work!)
        # just grab the first app on the screen.
        #
        x = self.UTILS.get_elements(*self.UTILS.verify("DOM.Market.featured_apps"))

        self.marionette.tap(x[0])   
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.app_details_header"))
        self.UTILS.TEST(x.text == p_app, "Expected title in app details to be '" + p_app + "', but was '" + x.text + "'.")
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Market.install_button"))
        self.marionette.tap(x)

        #
        # Confirm the installation of the web app.
        #
        self.marionette.switch_to_frame()

        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Market.confirm_install_button"))
        yes_button = self.marionette.find_element(*self.UTILS.verify("DOM.Market.confirm_install_button"))
        self.marionette.tap(yes_button)
        self.wait_for_element_not_displayed(*DOM.Market.confirm_install_button)

    #
    # Check the app is installed as an icon in the home screen (probably need to swipe right
    # to actually see it physically).
    #
    def verify_app_installed(self, p_app):            
        #
        # Go back to the home page and check the app is installed.
        #
        self.UTILS.TEST(self.UTILS.isAppInstalled(p_app), "App icon not found in homescreen.")
        
        
    
