#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from utils      import UTILS
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_gallery import *
from apps.app_camera import *

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
        
        #
        # TEST: Thumbnails are not visible when vieweing an image.
        #
        thumbs = self.UTILS.getElement(DOM.Gallery.thumbnail_list_section, "Thumbnail list section", False)
        self.UTILS.TEST( (thumbs.get_attribute("class") == "hidden"), "Thumbnails are not present when vieweing image in gallery.")
        
        #
        # TEST: Image is displayed as expected.
        #
        try: 
            thisIMG = self.UTILS.getElement(DOM.Gallery.current_image_pic, "Current image")
            try:
                x = str(thisIMG.get_attribute('src'))
                self.UTILS.TEST((x != ""), "Image source is not empty in gallery after clicking thumbnail.")
            except: 
                self.UTILS.logResult(False, "Image source exists in gallery after clicking thumbnail.")
        except: self.UTILS.logResult(False, "Image is displayed as expected after clicking icon in gallery.")
        
        #
        # Get a screenshot of the image from the galery thumbnail.
        #
        img_gallery_view = self.UTILS.screenShot("_GALLERY_VIEW")
        
        self.UTILS.logComment("PLEASE VERIFY THAT THESE ARE THE SAME IMAGE ... ")
        self.UTILS.logComment("    Before the capture button was pressed   : (unavailable)")
        self.UTILS.logComment("    Clicking the thumbnail in the camera app: " + img_thumb_view)
        self.UTILS.logComment("    Clicking the thumbnail in the gallery   : " + img_gallery_view)
