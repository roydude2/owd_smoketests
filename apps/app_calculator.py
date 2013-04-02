import DOM, time
from gaiatest   import GaiaTestCase
from utils      import UTILS
from marionette import Marionette
from apps.app_market import *
from apps.app_settings import *

class AppCalculator(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.Market     = AppMarket(p_parent)
        self.Settings   = AppSettings(p_parent)

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = UTILS(self)        
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
            self.Settings.turn_dataConn_on_if_required()
            self.Market.launch()
            self.Market.install_app("Calculator", "ndesaulniers")


    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Calculator')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");
