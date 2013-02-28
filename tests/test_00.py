#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings
from gaiatest import GaiaTestCase

class test_00(GaiaTestCase):
    _Description = "Install an app via 'everything.me'."
    
    _APP_NAME    = "CrystalSkull"
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 0)
        self.Settings   = app_settings.main(self, self.UTILS)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.data_layer.disable_wifi()
        self.data_layer.disable_cell_data()
        
        #
        # Make sure our app isn't installed already.
        #
        try:
            self.apps.uninstall(self.APP_NAME)
        except:
            ignoreme=1 # Do nothing.

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch Settings app.
        #
        self.Settings.launch()
        
        self.Settings.cellular_and_data()
        
        #
        # Wifi needs to be off for this test to work.
        #
        self.Settings.turn_dataConn_on(True)
        
        #
        # Go to the homescreen.
        #
        self.homescreen = self.apps.launch('Homescreen')
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.homescreen.frame)        

        #
        # Sweep right to expose the 'everything.me' screen.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')

        x = self.UTILS.get_elements(*DOM.EME.icons_groups)
        
        x[1].click()
        import time
        time.sleep(1)
        x[2].click()
        time.sleep(1)
        self.UTILS.savePageHTML("/tmp/roy1.html")

