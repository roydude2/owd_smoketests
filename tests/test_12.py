import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_gallery, app_camera
from gaiatest import GaiaTestCase

class test_12(GaiaTestCase):
    _Description = "Record a video and view it in the gallery app."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 12)
        self.gallery   = app_gallery.main(self, self.testUtils)
        self.camera    = app_camera.main(self, self.testUtils)
        
        #
        # Default timeout for finding elements on the screen.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
    
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordVideo("00:05")
        self.camera.testVideoLength(0, 4.9, 9.0)
       
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0)
        self.gallery.testVideoLength(4.9, 9.0)
        
        
        
        
