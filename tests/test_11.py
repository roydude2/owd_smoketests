import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_gallery, app_camera
from gaiatest import GaiaTestCase

class test_11(GaiaTestCase):
    _Description = "Take a photograph via the camera app."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 11)
        self.gallery   = app_gallery.main(self, self.testUtils)
        self.camera    = app_camera.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
            
    def tearDown(self):
        self.testUtils.reportResults()
        
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
        prev_marker = self.marionette.find_element(*DOM.Camera.thumbnail_preview_marker)
        self.testUtils.TEST((prev_marker.get_attribute("class") == "offscreen"), "Image was previewed as soon as picture was taken.")
        
        #
        # Click thumbnail.
        #
        self.camera.clickThumbnail(0)
        
        #
        # TEST: Thumbnail is previewed.
        #
        self.wait_for_element_displayed(*DOM.Camera.thumbnail_preview_marker)
        prev_marker = self.testUtils.get_element(*DOM.Camera.thumbnail_preview_marker)
        self.testUtils.TEST((prev_marker.get_attribute("class") == ""), "Image was not previewed when thumbnail was clicked.")
        
        #
        # Get a screenshot of the image from the camera preview thumbnail.
        #
        img_thumb_view = self.testUtils.screenShot("_THUMBNAIL_VIEW")
        
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
        thumbs = self.marionette.find_element(*DOM.Gallery.thumbnail_list_section)
        self.testUtils.TEST( (thumbs.get_attribute("class") == "hidden"), "Thumbnails still present when vieweing image in gallery.")
        
        #
        # TEST: Image is displayed as expected.
        #
        try: 
            thisIMG = self.testUtils.get_element(*DOM.Gallery.current_image_pic)
            try:
                x = str(thisIMG.get_attribute('src'))
                self.testUtils.TEST((x != ""), "Image source is empty in gallery after clicking thumbnail.")
            except: 
                self.testUtils.reportError("No image source in gallery after clicking thumbnail.")
        except: self.testUtils.reportError("Image not displayed as expected after clicking icon in gallery.")
        
        #
        # Get a screenshot of the image from the galery thumbnail.
        #
        img_gallery_view = self.testUtils.screenShot("_GALLERY_VIEW")
        
        self.testUtils.reportComment("PLEASE VERIFY THAT THESE ARE THE SAME IMAGE ... ")
        self.testUtils.reportComment("    Before the capture button was pressed   : (unavailable)")
        self.testUtils.reportComment("    Clicking the thumbnail in the camera app: " + img_thumb_view)
        self.testUtils.reportComment("    Clicking the thumbnail in the gallery   : " + img_gallery_view)
