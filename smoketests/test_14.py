
import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_gallery
from gaiatest import GaiaTestCase
import time

class test_11(GaiaTestCase):
    
    _img_list = ('IMG_001.jpg',
                 'IMG_002.jpg',
                 'IMG_003.jpg',
                 'IMG_004.jpg',
                 'IMG_005.jpg')
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = RoyUtils.testUtils(self, 14)
        self.gallery   = app_gallery.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
        
        #
        # Load sample images into the gallery.
        #
        for i in self._img_list:
            self.push_resource(i, 'DCIM/100MZLLA')
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
            
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Open each picture ...
        #
        for i in what?
            self.gallery.clickThumb(0, "pic")  
        
        #
        # TEST: Thumbnails are not visible when vieweing an image.
        #
        thumbs = self.marionette.find_element(*DOMS.Gallery.thumbnail_list_section)
        self.testUtils.TEST( (thumbs.get_attribute("class") == "hidden"), "Thumbnails still present when vieweing image in gallery.")
        
        #
        # TEST: Image is displayed as expected.
        #
        try: 
            thisIMG = self.testUtils.get_element(*DOMS.Gallery.current_image_pic)
            try:
                x = str(thisIMG.get_attribute('src'))
                self.testUtils.TEST((x == ""), "Image source is empty in gallery after clicking thumbnail.")
            except: 
                self.testUtils.reportError("No image source in gallery after clicking thumbnail.")
        except: self.testUtils.reportError("Image not displayed as expected after clicking icon in gallery.")
        
        #
        # Get a screenshot of the image from the galery thumbnail.
        #
        img1 = self.testUtils.screenShot("img_001.png")
        
        self.testUtils.reportComment("Please verify that these are the expected images (originals are in ./resources): ")
        self.testUtils.reportComment("    IMG_001.jpg: " + img1)
        self.testUtils.reportComment("    IMG_002.jpg: " + img2)
        self.testUtils.reportComment("    IMG_003.jpg: " + img3)
        self.testUtils.reportComment("    IMG_004.jpg: " + img4)
        self.testUtils.reportComment("    IMG_005.jpg: " + img5)
