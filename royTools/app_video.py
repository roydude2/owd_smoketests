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
        self.app = self.parent.apps.launch('Video')
        self.parent.wait_for_element_not_displayed(*DOMS.Video.items)
        
    def checkThumbDuration(self):
        self.testUtils.testFalse(
            (self.marionette.find_element(*DOMS.Video.duration_text).text == "00:00"), 
            "Video length was 0s.")

    def clickThumb(self, p_num):
        #
        # Get the list of video items and click the 'p_num' one.
        self.parent.wait_for_element_displayed(*DOMS.Video.items)
        all_videos = self.marionette.find_elements(*DOMS.Video.items)
        my_video = all_videos[p_num]
        
        self.marionette.tap(my_video)
        
        #
        # Video is automatically played.
        #
        self.parent.wait_for_element_displayed(*DOMS.Video.video_frame)
        self.parent.wait_for_element_displayed(*DOMS.Video.video_loaded)

    def checkPlayDuration(self):
        # The elapsed time != 00:00 
        self.testUtils.testFalse((self.marionette.find_element(*DOMS.Video.elapsed_text).text == "00:00"), "Video length was 0s.")
