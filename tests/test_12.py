#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_12(GaiaTestCase):
    _Description = "Record a video and view it in the gallery app."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.gallery    = AppGallery(self)
        self.camera     = AppCamera(self)
        
        #
        # Default timeout for finding elements on the screen.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
    
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordVideo("00:05")
        self.camera.checkVideoLength(0, 4.9, 10.0)
       
        #
        # Open the gallery application.
        #
        self.UTILS.goHome()
        self.gallery.launch()
        
        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0)
        self.gallery.checkVideoLength(4.9, 10.0)
        
        
        
        
