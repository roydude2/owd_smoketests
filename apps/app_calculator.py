import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette
from apps.app_market import *

class AppCalculator(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.Market     = AppMarket(p_parent)

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS
        
        #
        # Sometimes the calcultaor gets uninstalled!
        #
        if not self.UTILS.isAppInstalled("Calculator"):
            self.UTILS.logComment("Calculator was installed automatically because it was missing.")
            
            #
            # There are a few 'Calculator' apps, so make sure we get the correct
            # one.
            #
            self.Market.launch()
            self.Market.install_app("Calculator", "ndesaulniers")


    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Calculator')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)
