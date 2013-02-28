import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_settings
from gaiatest import GaiaTestCase
import os, time

class test_00(GaiaTestCase):
    _Description = "(Just a place to work things out :)"
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 00)
        self.Settings  = app_settings.main(self, self.testUtils)
        #self.testWIFI  = self.testUtils.get_os_variable("ROYWANTSYOURWIFI", "Enter the wifi network name (case sensitive)")

        self.marionette.set_search_timeout(50)
            
    def tearDown(self):
        self.testUtils.reportResults()

        
    def test_run(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script(
            'navigator.mozApps.install("%s")' % "Calculator")
