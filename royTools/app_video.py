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
        #self.parent.wait_for_element_not_displayed(*DOMS.Video.items)
        self.parent.wait_for_element_not_displayed(*DOMS.Video.items)
        
    def checkThumbDuration(self, p_expected):
        self.parent.wait_for_element_present(*DOMS.Video.thumb_durations)
        durations = self.marionette.find_elements(*DOMS.Video.thumb_durations)
        
        myDur = durations[0].text
        
        self.testUtils.TEST(myDur == p_expected, 
            "Video length on thumbnail was %s, but should have been %s." % (myDur, p_expected))

    def clickThumb(self, p_num):
        #
        # Get the list of video items and click the 'p_num' one.
        #
        self.parent.wait_for_element_displayed(*DOMS.Video.items)
        all_videos = self.marionette.find_elements(*DOMS.Video.items)
        my_video = all_videos[p_num]
        
        self.marionette.tap(my_video)
        
        #
        # Video is automatically played.
        #
        self.parent.wait_for_element_displayed(*DOMS.Video.video_frame)
        self.parent.wait_for_element_displayed(*DOMS.Video.video_loaded)

    def checkPlayDuration(self, p_from, p_to):
        #x = self.marionette.find_element(*DOMS.Video.video_loaded)
        #self.marionette.tap(x)
        start_time = time.time()
        self.parent.wait_for_element_not_displayed(*DOMS.Video.video_loaded)
        elapsed_time = int(time.time() - start_time)
        
        # Check time was between p_from and p_to.
        x = self.testUtils.TEST((elapsed_time > p_from & elapsed_time < p_to), 
            "Video played in %.2f seconds, when it should have been between %d and %d seconds." % (elapsed_time, p_from, p_to))
