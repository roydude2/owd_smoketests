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
        self.app = self.parent.apps.launch('Video')
        self.parent.wait_for_element_not_displayed(*DOM.Video.items)
        
    #
    # NOTE: p_length_str_MMSS needs to be in the format "MM:SS"
    #
    def checkThumbDuration(self, p_thumb_num, p_length_str_MMSS, p_errorMargin_SS):
        self.parent.wait_for_element_present(*DOM.Video.thumb_durations)
        durations = self.marionette.find_elements(*DOM.Video.thumb_durations)
        
        myDur = durations[p_thumb_num].text
        
        if myDur == p_length_str_MMSS:
            self.testUtils.TEST(1==1, "Just a marker to show we tested here.")
        else:
            #
            # Video length didn't match exactly, but is it within the acceptable error margin?
            #
            from datetime import datetime, timedelta
            
            x_t = datetime.strptime(myDur, '%M:%S')
            y_t = datetime.strptime(p_length_str_MMSS, '%M:%S')
            
            in_errorMargin = False
            
            # Less than?
            if y_t == (x_t - timedelta(seconds=p_errorMargin_SS)):
                in_errorMargin = True

            # More than?
            if y_t == (x_t + timedelta(seconds=p_errorMargin_SS)):
                in_errorMargin = True
            
        self.testUtils.TEST(in_errorMargin, 
            "Expected video length on thumbnail to be %s (within %s seconds), but it was %s." % (p_length_str_MMSS, p_errorMargin_SS, myDur))

    #
    # Clicks the thumbnail to start the video.
    #
    def startVideo(self, p_num):
        #
        # Get the list of video items and click the 'p_num' one.
        #
        self.parent.wait_for_element_displayed(*DOM.Video.items)
        all_videos = self.marionette.find_elements(*DOM.Video.items)
        my_video = all_videos[p_num]
        
        self.marionette.tap(my_video)

        #
        # Wait for the video to start playing before returning.
        #
        self.parent.wait_for_element_displayed(*DOM.Video.video_frame)
        self.parent.wait_for_element_displayed(*DOM.Video.video_loaded)

        #
        # Allow for bug - if video plays without screen being tapped, then when
        # it finishes the player closes (and marionette crashes).
        #
        self.testUtils.reportComment(
            "BUG IN VIDEO PLAYER: Sometimes crashes after playing a video! " + 
            "If you see an error dumped by Marionette here, it's probably because of that.")
        #x=self.marionette.find_element(*DOM.Video.video_loaded)
        #self.marionette.tap(x)
        
    #
    # Check the length of a video.
    #
    def testVideoLength(self, p_vid_num, p_from_SS, p_to_SS):
            
        #
        # Start the timer.
        #
        start_time = time.time()
        
        #
        # Play the video.
        #
        self.startVideo(p_vid_num)
        
        #
        # Stop the timer.
        #
        self.parent.wait_for_element_not_displayed(*DOM.Video.video_frame)
        elapsed_time = int(time.time() - start_time)
        
        #
        # Check the elapsed time.
        #
        self.testUtils.TEST((elapsed_time > p_from_SS), "Video is shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.testUtils.TEST((elapsed_time < p_to_SS), "Video is longer than expected (played for %.2f seconds)." % elapsed_time)
