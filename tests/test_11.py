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

class test_11(GaiaTestCase):
    _Description = "Take a picture with camera."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.gallery    = AppGallery(self)
        self.camera     = AppCamera(self)

        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
            
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Start the camera application.
        #
        self.camera.launch()

        #
        # Take a picture.
        #
        self.camera.takePicture()
        
        #
        # TEST: Thumbnail has not been previewed yet.
        #
        prev_marker = self.UTILS.getElement(DOM.Camera.thumbnail_preview_marker, "Thumbnail preview marker", False)
        self.UTILS.TEST((prev_marker.get_attribute("class") == "offscreen"), 
                        "Image is not previewed as soon as picture is taken.")
        
        #
        # Click thumbnail.
        #
        self.camera.clickThumbnail(0)
        
        #
        # TEST: Thumbnail is previewed.
        #
        prev_marker = self.UTILS.getElement(DOM.Camera.thumbnail_preview_marker, "Thumbnail preview marker", False)
        self.UTILS.TEST((prev_marker.get_attribute("class") == ""), "Image is previewed when thumbnail is clicked.")
        
        #
        # Get a screenshot of the image from the camera preview thumbnail.
        #
        img_thumb_view = self.UTILS.screenShot("_THUMBNAIL_VIEW")
        
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0)
        
