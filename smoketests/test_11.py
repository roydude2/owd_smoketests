import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_gallery, app_camera
from gaiatest import GaiaTestCase
import time

class test_11(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = RoyUtils.testUtils(self, 11)
        self.gallery   = app_gallery.main(self, self.testUtils)
        self.camera    = app_camera.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
            
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
        prev_marker = self.marionette.find_element(*DOMS.Camera.thumbnail_preview_marker)
        self.testUtils.testTrue((prev_marker.get_attribute("class") == "offscreen"), "Image was previewed as soon as picture was taken.")
        
        #
        # Click thumbnail.
        #
        self.camera.clickThumbnail(0)
        
        #
        # TEST: Thumbnail is previewed.
        #
        self.wait_for_element_displayed(*DOMS.Camera.thumbnail_preview_marker)
        prev_marker = self.testUtils.get_element(*DOMS.Camera.thumbnail_preview_marker)
        self.testUtils.testTrue((prev_marker.get_attribute("class") == ""), "Image was not previewed when thumbnail was clicked.")
        
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
        self.gallery.clickThumb(0, "pic")
        
        #
        # TEST: Thumbnails are not visible when vieweing an image.
        #
        thumbs = self.marionette.find_element(*DOMS.Gallery.thumbnail_list_section)
        self.testUtils.testTrue( (thumbs.get_attribute("class") == "hidden"), "Thumbnails still present when vieweing image in gallery.")
        
        #
        # TEST: Image is displayed as expected.
        #
        try: 
            thisIMG = self.testUtils.get_element(*DOMS.Gallery.current_image_pic)
            try:
                x = str(thisIMG.get_attribute('src'))
                self.testUtils.testFalse((x == ""), "Image source is empty in gallery after clicking thumbnail.")
            except: 
                self.testUtils.testTrue( (1==2), "No image source in gallery after clicking thumbnail.")
        except: self.testUtils.testTrue( (1==2), "Image not displayed as expected after clicking icon in gallery.")
        
        #
        # Get a screenshot of the image from the galery thumbnail.
        #
        img_gallery_view = self.testUtils.screenShot("_GALLERY_VIEW")
        
        self.testUtils.reportComment("Please verify that these are the same image: ")
        self.testUtils.reportComment("    Before the capture button was pressed   : (unavailable)")
        self.testUtils.reportComment("    Clicking the thumbnail in the camera app: " + img_thumb_view)
        self.testUtils.reportComment("    Clicking the thumbnail in the gallery   : " + img_gallery_view)
