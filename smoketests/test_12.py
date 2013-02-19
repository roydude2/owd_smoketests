import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_gallery, app_camera
from gaiatest import GaiaTestCase
import time

class test_12(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = RoyUtils.testUtils(self, 12)
        self.gallery   = app_gallery.main(self, self.testUtils)
        self.camera    = app_camera.main(self, self.testUtils)
        
        # Default timeout for finding elements on the screen.
        self.marionette.set_search_timeout(50)
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
    
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordAVideo()
        self.camera.testVideo()
       
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0, "vid")
        
        self.gallery.playCurrentVideo()
        
        
        
        
