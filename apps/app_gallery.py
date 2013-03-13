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
        self.UTILS      = TestUtils(self, 00)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS


    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Gallery')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    def thumbCount(self):
        self.wait_for_element_present(*self.UTILS.verify("DOM.Gallery.thumbnail_items"))
        x = self.marionette.find_elements(*self.UTILS.verify("DOM.Gallery.thumbnail_items"))
        return len(x)

    #
    # Returns a list of gallery item objects.
    #
    def getGalleryItems(self):
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Gallery.thumbnail_items"))
        return self.marionette.execute_script("return window.wrappedJSObject.files;")
        
    def clickThumb(self, p_num):
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == p_num:
                my_item = self.marionette.find_elements(*self.UTILS.verify("DOM.Gallery.thumbnail_items"))[index]
                self.marionette.tap(my_item)

                if 'video' in item['metadata']:
                    self.wait_for_element_displayed(*self.UTILS.verify("DOM.Gallery.current_image_vid"))
                else:
                    self.wait_for_element_displayed(*self.UTILS.verify("DOM.Gallery.current_image_pic"))
                break

        #self.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
        #all_items = self.marionette.find_elements(*DOM.Gallery.thumbnail_items)
        #my_item = all_items[p_num]
        #self.marionette.tap(my_item)
        

    #
    # Plays the video we've loaded (in gallery you have to click the thumbnail first,
    # THEN press a play button - it doesn't play automatically).
    #
    def playCurrentVideo(self):
        self.wait_for_element_displayed(*self.UTILS.verify("DOM.Gallery.video_play_button"))
        playBTN = self.marionette.find_element(*self.UTILS.verify("DOM.Gallery.video_play_button"))
        playBTN.click()
        self.marionette.tap(playBTN)
        self.wait_for_element_not_displayed(*self.UTILS.verify("DOM.Gallery.video_pause_button"))

    #
    # Check the length of a video.
    #
    def checkVideoLength(self, p_from_SS, p_to_SS):
            
        # Start the timer.
        start_time = time.time()
        
        # Play the video.
        self.playCurrentVideo()
        
        # Stop the timer.
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is longer than expected (played for %.2f seconds)." % elapsed_time)
