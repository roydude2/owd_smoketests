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
        self.UTILS = TestUtils(self, 14)
        self.gallery   = app_gallery.main(self, self.UTILS)

        self.marionette.set_search_timeout(50)
        
        #
        # Load sample images into the gallery.
        #
        for i in self._img_list:
            self.push_resource(i, destination='DCIM/100MZLLA')
            
    def tearDown(self):
        self.UTILS.reportResults()
        
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
            self.UTILS.reportComment("PLEASE VERIFY THE FOLLOWING " + str(x) + " IMAGES ....")
            for i in range(0, x):
                # Click this thumbnail.
                self.gallery.clickThumb(i)
                
                # Take a screenshot (and update the comment).
                imgnam = self.UTILS.screenShot("14_" + str(i))
                self.UTILS.reportComment("-> " + imgnam)
                
                # Check the size of the screenshot.
                # (because we can't guarentee the order, or match the filenames, we have to just loop through our
                # known sizes to see if this one's in there.
                img_size     = os.path.getsize(imgnam)
                size_matched = False
                for this_size in self._img_sizes:
                    if img_size == this_size:
                        size_matched = True
                        break
                        
                self.UTILS.TEST(size_matched,
                    "Unexpected image size (" + str(self._img_sizes[i]) + " bytes). please visually check the screenshots.")
                
                # Wait a second (or this test is done too quickly to see!)
                time.sleep(0.5)
                
                # Go back to the thumbnails.
                backBTN = self.marionette.find_element(*DOM.Gallery.fullscreen_back_button)
                self.marionette.tap(backBTN)
                self.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
        

