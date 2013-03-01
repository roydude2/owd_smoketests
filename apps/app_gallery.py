from apps import DOM
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.UTILS  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.parent.apps.kill_all()
        self.app = self.parent.apps.launch('Gallery')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    def thumbCount(self):
        self.parent.wait_for_element_present(*DOM.Gallery.thumbnail_items)
        x = self.marionette.find_elements(*DOM.Gallery.thumbnail_items)
        return len(x)

    #
    # Returns a list of gallery item objects.
    #
    def getGalleryItems(self):
        self.parent.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
        return self.marionette.execute_script("return window.wrappedJSObject.files;")
        
    def clickThumb(self, p_num):
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == p_num:
                my_item = self.marionette.find_elements(*DOM.Gallery.thumbnail_items)[index]
                self.marionette.tap(my_item)

                if 'video' in item['metadata']:
                    self.parent.wait_for_element_displayed(*DOM.Gallery.current_image_vid)
                else:
                    self.parent.wait_for_element_displayed(*DOM.Gallery.current_image_pic)
                break

        #self.parent.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
        #all_items = self.marionette.find_elements(*DOM.Gallery.thumbnail_items)
        #my_item = all_items[p_num]
        #self.marionette.tap(my_item)
        

    #
    # Plays the video we've loaded (in gallery you have to click the thumbnail first,
    # THEN press a play button - it doesn't play automatically).
    #
    def playCurrentVideo(self):
        self.parent.wait_for_element_displayed(*DOM.Gallery.video_play_button)
        playBTN = self.marionette.find_element(*DOM.Gallery.video_play_button)
        playBTN.click()
        self.marionette.tap(playBTN)
        self.parent.wait_for_element_not_displayed(*DOM.Gallery.video_pause_button)

    #
    # Check the length of a video.
    #
    def testVideoLength(self, p_from_SS, p_to_SS):
            
        # Start the timer.
        start_time = time.time()
        
        # Play the video.
        self.playCurrentVideo()
        
        # Stop the timer.
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is longer than expected (played for %.2f seconds)." % elapsed_time)
