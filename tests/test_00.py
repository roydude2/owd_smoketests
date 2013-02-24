import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_gallery
from gaiatest import GaiaTestCase
import os, time

class test_00(GaiaTestCase):
    _Description = "(Just a place to work things out :)"
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 00)
        self.MYAPP   = app_gallery.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
            
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Open the gallery application.
        #
        self.MYAPP.launch()
        
        self.testUtils.reportComment("RESOURCE: " + self.resource("kjkhkhjkgk"))
        
        return
        
        #
        # Tap App permissions.
        #
        x = self.marionette.find_element(*DOM.Settings.app_permissions)
        self.marionette.tap(x)
        
        #
        # Tap Camera.
        #
        self.wait_for_element_displayed(*DOM.Settings.app_perm_camera)
        x = self.marionette.find_element(*DOM.Settings.app_perm_camera)
        self.marionette.tap(x)
        
        #
        # Tap Geolocation.
        #
        self.wait_for_element_displayed(*DOM.Settings.app_perm_camera_geo)
        x = self.marionette.find_element(*DOM.Settings.app_perm_camera_geo)
        self.marionette.tap(x)

        time.sleep(5)
        self.marionette.switch_to_frame()
        self.testUtils.reportComment("Listing frames from 1 ...")
        self.testUtils.list_iframes()
        self.testUtils.reportComment("Listing frames from 2 ...")
        self.testUtils.list_iframes()
        self.testUtils.reportComment("Listing window handlers ... :" + self.marionette.current_window_handle)
        now_available = self.marionette.window_handles
        for win in now_available:
            self.testUtils.reportComment("")
            self.testUtils.reportComment(str(win))
        self.testUtils.savePageHTML("/tmp/roy1.html")
