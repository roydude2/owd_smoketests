from apps import DOM
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.testUtils  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.app = self.parent.apps.launch('Gallery')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    def clickThumb(self, p_num, p_type):
        self.parent.wait_for_element_displayed(*DOM.Gallery.items)
        all_items = self.marionette.find_elements(*DOM.Gallery.items)
        my_item = all_items[p_num]
        self.marionette.tap(my_item)
        
        if p_type.lower() == "vid":
            self.parent.wait_for_element_displayed(*DOM.Gallery.current_image_vid)
        else:
            self.parent.wait_for_element_displayed(*DOM.Gallery.current_image_pic)

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
        
        self.testUtils.TEST((elapsed_time > p_from_SS), "Video is shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.testUtils.TEST((elapsed_time < p_to_SS), "Video is longer than expected (played for %.2f seconds)." % elapsed_time)
