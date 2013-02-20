from royTools import DOMS
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
        self.app = self.parent.apps.launch('Camera')
        self.parent.wait_for_element_not_displayed(*DOMS.GLOBAL.loading_overlay)
        
    def switchSource(self):
        switchBTN = self.testUtils.get_element(*DOMS.Camera.switch_source_btn)
        self.marionette.tap(switchBTN)        
        self.parent.wait_for_element_present(*DOMS.Camera.capture_button_enabled)

    #
    # Take a picture.
    #
    def takePicture(self):
        x = self.testUtils.get_element(*DOMS.Camera.capture_button)
        self.marionette.tap(x)
        self.parent.wait_for_element_displayed(*DOMS.Camera.thumbnail)
        
    #
    # Click thumbnail.
    #
    def clickThumbnail(self, p_num):
        thumbEl = self.marionette.find_element(*DOMS.Camera.thumbnail)
        self.marionette.tap(thumbEl)

    #
    # Check the length of a video.
    #
    def testVideo(self):
            
        #
        # Find the thumbnail for this video and click it.
        #
        self.clickThumbnail(0)
        
        #
        # Click the button to play the video and make sure it takes between
        # 5 and 9 seconds to complete (to allow time delay in element
        # loading).
        #
        playBTN = self.testUtils.get_element(*DOMS.Camera.video_play_button)
        self.marionette.tap(playBTN)

        # Start the timer when the pause button is visible.
        self.parent.wait_for_element_displayed(*DOMS.Camera.video_pause_button)
        start_t = time.time()
        
        # Stop the timer when the pause button is no longer visible.
        self.parent.wait_for_element_not_displayed(*DOMS.Camera.video_pause_button)
        end_t = time.time()
        
        timeDiff = (end_t - start_t)
        
        self.testUtils.TEST((timeDiff > 4.90), "5 second video is shorter than expected (finished playing in %.2f seconds)." % timeDiff)
        self.testUtils.TEST((timeDiff < 9.00), "5 second video is longer than expected (finished playing in %.2f seconds)." % timeDiff)

    def recordAVideo(self):
        self.testUtils.reportComment("(I still need to figure out how to suppress gps question.)")

        #
        # Switch to video.
        #
        self.switchSource()

        #
        # Record a video and click the thumbnail to play it.
        #
        captureBTN = self.testUtils.get_element(*DOMS.Camera.capture_button)
        self.marionette.tap(captureBTN)
        
        # Record for 5 seconds
        self.parent.wait_for_condition(lambda m: m.find_element(*DOMS.Camera.video_timer).text == '00:05')

        # Stop recording
        self.marionette.tap(captureBTN)
        self.parent.wait_for_element_not_displayed(*DOMS.Camera.video_timer)

        self.parent.wait_for_element_displayed(*DOMS.Camera.thumbnail)
        
        # TEST: Thumbnail has not been previewed yet.
        prev_marker = self.parent.marionette.find_element(*DOMS.Camera.thumbnail_preview_marker)
        self.testUtils.TEST((prev_marker.get_attribute("class") == "offscreen"), "Image was previewed as soon as picture was taken.")
        



