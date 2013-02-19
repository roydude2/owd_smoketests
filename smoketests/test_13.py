import sys
sys.path.append("./")

from royTools import RoyUtils, DOMS, app_camera, app_video
from gaiatest import GaiaTestCase
import time

class test_13(GaiaTestCase):
    
    def setUp(self):
        GaiaTestCase.setUp(self)
        self.testUtils = RoyUtils.testUtils(self, 13)
        self.camera    = app_camera.main(self, self.testUtils)
        self.video     = app_video.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        
        # Unlock the screen (if necessary)
        self.testUtils.unlockScreen()
    
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordAVideo()
        self.camera.testVideo()
       
        #
        # Open the video player application.
        #
        self.video.launch()
        
        #
        # the first thumbnail should be our video.
        #
        self.video.checkThumbDuration()
        self.video.clickThumb(0)
        
        #
        # Check that the video is as long as expected.
        #
        self.video.checkPlayDuration()
        
        #
        # Wait for the video to finsih before proceeding.
        #
        self.wait_for_element_not_displayed(*DOMS.Video.video_frame)
