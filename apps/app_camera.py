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
        
        #
        # Default to not prompting for geolocation.
        #
        self.parent.apps.set_permission('Camera', 'geolocation', 'deny')

    def launch(self):
        self.app = self.parent.apps.launch('Camera')
        self.parent.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)
        
    def switchSource(self):
        switchBTN = self.testUtils.get_element(*DOM.Camera.switch_source_btn)
        self.marionette.tap(switchBTN)        
        self.parent.wait_for_element_present(*DOM.Camera.capture_button_enabled)

    #
    # Take a picture.
    #
    def takePicture(self):
        x = self.testUtils.get_element(*DOM.Camera.capture_button)
        self.marionette.tap(x)
        self.parent.wait_for_element_displayed(*DOM.Camera.thumbnail)
        
    #
    # Click thumbnail.
    #
    def clickThumbnail(self, p_num):
        thumbEls = self.marionette.find_elements(*DOM.Camera.thumbnail)
        myThumb = thumbEls[p_num]
        self.marionette.tap(myThumb)

    #
    # Check the length of a video.
    #
    def testVideoLength(self, p_vid_num, p_from_SS, p_to_SS):
            
        #
        # Find the thumbnail for this video and click it.
        #
        self.clickThumbnail(p_vid_num)
        
        #
        # Click the button to play the video and make sure it takes between
        # 5 and 9 seconds to complete (to allow time delay in element
        # loading).
        #
        playBTN = self.testUtils.get_element(*DOM.Camera.video_play_button)
        self.marionette.tap(playBTN)

        # Start the timer when the pause button is visible.
        self.parent.wait_for_element_displayed(*DOM.Camera.video_pause_button)
        start_time = time.time()
        
        # Stop the timer when the pause button is no longer visible.
        self.parent.wait_for_element_not_displayed(*DOM.Camera.video_pause_button)
        
        elapsed_time = int(time.time() - start_time)
        
        self.testUtils.TEST((elapsed_time > p_from_SS), "Video is shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.testUtils.TEST((elapsed_time < p_to_SS), "Video is longer than expected (played for %.2f seconds)." % elapsed_time)

    #
    # NOTE: p_length needs to be in the format "mm:ss"
    #
    def recordVideo(self, p_length_str_MMSS):
        #
        # Switch to video.
        #
        self.switchSource()

        #
        # Record a video and click the thumbnail to play it.
        #
        captureBTN = self.testUtils.get_element(*DOM.Camera.capture_button)
        self.marionette.tap(captureBTN)
        
        # Record for 5 seconds
        self.parent.wait_for_condition(lambda m: m.find_element(*DOM.Camera.video_timer).text == p_length_str_MMSS)

        # Stop recording
        self.marionette.tap(captureBTN)
        self.parent.wait_for_element_not_displayed(*DOM.Camera.video_timer)

        self.parent.wait_for_element_displayed(*DOM.Camera.thumbnail)
        
        # TEST: Thumbnail has not been previewed yet.
        prev_marker = self.parent.marionette.find_element(*DOM.Camera.thumbnail_preview_marker)
        self.testUtils.TEST((prev_marker.get_attribute("class") == "offscreen"), "Image was previewed as soon as picture was taken.")
        



