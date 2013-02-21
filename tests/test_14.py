import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_gallery
from gaiatest import GaiaTestCase

class test_14(GaiaTestCase):
    _Description = "Viewing images in the gallery app."
    
    _img_list = ('resources/img1.jpg',
                 'resources/img2.jpg',
                 'resources/img3.jpg',
                 'resources/img4.jpg',
                 'resources/img5.jpg')
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 14)
        self.gallery   = app_gallery.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
        
        #
        # Load sample images into the gallery.
        #
        #for i in self._img_list:
            #self.push_resource(i, 'DCIM/100MZLLA')
        
        #self.push_resource('img1.jpg', count=700, destination='DCIM/100MZLLA')
        import os
        x = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', 'img1.jpg'))
        self.testUtils.reportComment("X: " + x)
        self.push_resource('img1.jpg', destination='DCIM/100MZLLA')
            
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        ##
        ## Open each picture ...
        ##
        #for i in what?
            #self.gallery.clickThumb(0, "pic")  
        
        ##
        ## TEST: Thumbnails are not visible when vieweing an image.
        ##
        #thumbs = self.marionette.find_element(*DOM.Gallery.thumbnail_list_section)
        #self.testUtils.TEST( (thumbs.get_attribute("class") == "hidden"), "Thumbnails still present when vieweing image in gallery.")
        
        ##
        ## TEST: Image is displayed as expected.
        ##
        #try: 
            #thisIMG = self.testUtils.get_element(*DOM.Gallery.current_image_pic)
            #try:
                #x = str(thisIMG.get_attribute('src'))
                #self.testUtils.TEST((x == ""), "Image source is empty in gallery after clicking thumbnail.")
            #except: 
                #self.testUtils.reportError("No image source in gallery after clicking thumbnail.")
        #except: self.testUtils.reportError("Image not displayed as expected after clicking icon in gallery.")
        
        ##
        ## Get a screenshot of the image from the galery thumbnail.
        ##
        #img1 = self.testUtils.screenShot("img_001.png")
        
        #self.testUtils.reportComment("Please verify that these are the expected images (originals are in ./resources): ")
        #self.testUtils.reportComment("    img1.jpg: " + img1)
        #self.testUtils.reportComment("    img2.jpg: " + img2)
        #self.testUtils.reportComment("    img3.jpg: " + img3)
        #self.testUtils.reportComment("    img4.jpg: " + img4)
        #self.testUtils.reportComment("    img5.jpg: " + img5)
