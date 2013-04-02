import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppGallery(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS


    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Gallery')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay stops being displayed");

    def thumbCount(self):
        x = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails", False)
        return len(x)

    def getGalleryItems(self):
        #
        # Returns a list of gallery item objects.
        #
        self.UTILS.waitForElements(DOM.Gallery.thumbnail_items, "Thumbnails", True, 20, False)
        return self.marionette.execute_script("return window.wrappedJSObject.files;")
        
    def clickThumb(self, p_num):
        #
        # Clicks a thumbnail from the gallery.
        #
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == p_num:
                my_item = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery item list", True, 20, False)[index]
                self.marionette.tap(my_item)

                if 'video' in item['metadata']:
                    self.UTILS.waitForElements(DOM.Gallery.current_image_vid, "Video playing", True, 20, False)
                else:
                    self.UTILS.waitForElements(DOM.Gallery.current_image_pic, "Image", True, 20, False)
                break

    def playCurrentVideo(self):
        #
        # Plays the video we've loaded (in gallery you have to click the thumbnail first,
        # THEN press a play button - it doesn't play automatically).
        #
        playBTN = self.UTILS.getElement(DOM.Gallery.video_play_button, "Video play button")
        playBTN.click()
        self.marionette.tap(playBTN)
        
        self.UTILS.waitForNotElements(DOM.Gallery.video_pause_button, "Pause button", True, 20, False);

    def checkVideoLength(self, p_from_SS, p_to_SS):
        #
        # Check the length of a video.
        #
            
        # Start the timer.
        start_time = time.time()
        
        # Play the video.
        self.playCurrentVideo()
        
        # Stop the timer.
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)
