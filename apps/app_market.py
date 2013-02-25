from apps import DOM
import time

class main():

    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.testUtils  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.app = self.parent.apps.launch('Marketplace')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    #
    # Install an app.
    #
    def install_app(self, p_app):
        #
        # Because of the change to the search (and the fact that I can't get Marionette 'flick()' to work!)
        # just grab the first app on the screen.
        #
        x = self.testUtils.get_elements(*DOM.Market.featured_apps)

        self.marionette.tap(x[0])   
        
        x = self.testUtils.get_element(*DOM.Market.app_details_header)
        self.testUtils.TEST(x.text == p_app, "Expected title in app details to be '" + p_app + "', but was '" + x.text + "'.")
        
        x = self.testUtils.get_element(*DOM.Market.install_button)
        self.marionette.tap(x)

        #
        # Confirm the installation of the web app.
        #
        self.marionette.switch_to_frame()

        self.parent.wait_for_element_displayed(*DOM.Market.confirm_install_button)
        yes_button = self.marionette.find_element(*DOM.Market.confirm_install_button)
        self.marionette.tap(yes_button)
        self.parent.wait_for_element_not_displayed(*DOM.Market.confirm_install_button)

    #
    # Check the app is installed as an icon in the home screen (probably need to swipe right
    # to actually see it physically).
    #
    def verify_app_installed(self, p_app):            
        #
        # Not sure why, but this is different to "self.marionette.switch_to_frame()".
        #
        homescreen_frame = self.marionette.find_element(*DOM.GLOBAL.homescreen_iframe)
        self.marionette.switch_to_frame(homescreen_frame)
        
        app_icon_locator = ('xpath', DOM.GLOBAL.homescreen_app_icons % p_app)
        try:
            self.parent.wait_for_element_present(*app_icon_locator)
        except:
            self.testUtils.TEST(1==2, "Could not find app icon on the home screen after install!", True)
            
        self.testUtils.TEST(1==1, "Just a marker to show we tested for this!")
    
