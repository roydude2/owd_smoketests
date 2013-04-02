import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppVideo(GaiaTestCase):
    
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
        self.app = self.apps.launch('Video')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");
        
    def checkThumbDuration(self, p_thumb_num, p_length_str_MMSS, p_errorMargin_SS):
        #
        # NOTE: p_length_str_MMSS needs to be in the format "MM:SS"
        #
        self.UTILS.waitForElements(DOM.Video.thumb_durations, "Video thumbnail duration appears.", True, 20, False)

        durations = self.UTILS.getElements(DOM.Video.thumb_durations, "Thumbnail durations")
        
        myDur = durations[p_thumb_num].text
        
        #
        # Video length didn't match exactly, but is it within the acceptable error margin?
        #
        from datetime import datetime, timedelta
        
        actual_time = datetime.strptime(myDur, '%M:%S')
        expect_time = datetime.strptime(p_length_str_MMSS, '%M:%S')
        margin_time = timedelta(seconds=p_errorMargin_SS)
        
        diff_time   = actual_time - expect_time
        
        in_errorMargin = False
            
        # Less than expected, but within the error margin?
        if margin_time >= diff_time:
            in_errorMargin = True
            
        self.UTILS.TEST(in_errorMargin, 
            "Expected video length on thumbnail to be %s, +- %s seconds (it was %s seconds)." % 
                (p_length_str_MMSS, p_errorMargin_SS, myDur))

    def startVideo(self, p_num):
        #
        # Clicks the thumbnail to start the video.
        #

        #
        # Get the list of video items and click the 'p_num' one.
        #
        all_videos = self.UTILS.getElements(DOM.Video.items, "Videos")
        my_video = all_videos[p_num]
        self.marionette.tap(my_video)

        #
        # Wait for the video to start playing before returning.
        #
        self.UTILS.waitForElements(DOM.Video.video_loaded, "Loaded video", True, 20, False)

        
    def checkVideoLength(self, p_vid_num, p_from_SS, p_to_SS):
        #
        # Check the length of a video by playing it.
        #
            
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
#        self.wait_for_element_not_displayed(*DOM.Video.video_frame)
        self.UTILS.waitForNotElements(DOM.Video.video_frame, "Video frame", True, 20, False);
        elapsed_time = int(time.time() - start_time)
        
        #
        # Check the elapsed time.
        #
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)
