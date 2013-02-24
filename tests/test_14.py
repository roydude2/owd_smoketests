import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_gallery
from gaiatest import GaiaTestCase
import os, time

class test_14(GaiaTestCase):
    _Description = "Viewing images in the gallery app."
    
    _img_list = ('img1.jpg',
                 'img2.jpg',
                 'img3.jpg',
                 'img4.jpg',
                 'img5.jpg')
                 
    _img_sizes = (68056,51735,47143,59955,60352)

    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 14)
        self.gallery   = app_gallery.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
        
        #
        # Load sample images into the gallery.
        #
        for i in self._img_list:
            self.push_resource(i, destination='DCIM/100MZLLA')
            
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Takes a few seconds for the thumbs to appear...
        #
        time.sleep(8)
        
        #
        # Open each picture ...
        #
        x = self.gallery.thumbCount()
        if x > 0:
            self.testUtils.reportComment("PLEASE VERIFY THE FOLLOWING " + str(x) + " IMAGES ....")
            for i in range(0, x):
                # Click this thumbnail.
                self.gallery.clickThumb(i)
                
                # Take a screenshot (and update the comment).
                imgnam = self.testUtils.screenShot("14_" + str(i))
                self.testUtils.reportComment("-> " + imgnam)
                
                # Check the size of the screenshot.
                img_size = os.path.getsize(imgnam)
                self.testUtils.TEST((img_size == self._img_sizes[i]),
                    "Expected image " + str (i) + " to be " + str(self._img_sizes[i]) + " bytes, but was " + str(img_size))
                
                # Wait a second (or this test is done too quickly to see!)
                time.sleep(0.5)
                
                # Go back to the thumbnails.
                backBTN = self.marionette.find_element(*DOM.Gallery.fullscreen_back_button)
                self.marionette.tap(backBTN)
                self.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
        

