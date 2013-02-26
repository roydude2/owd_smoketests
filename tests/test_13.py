import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_camera, app_video
from gaiatest import GaiaTestCase

class test_13(GaiaTestCase):
    _Description = "Record video and view it in the video player app."
    
    def setUp(self):
        #
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 13)
        self.camera    = app_camera.main(self, self.testUtils)
        self.video     = app_video.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
    
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordVideo("00:05")
        self.camera.testVideoLength(0, 4.9, 9.0)

        #
        # Open the video player application.
        #
        self.video.launch()
        
        #
        # the first thumbnail should be our video.
        #
        self.video.checkThumbDuration(0, "00:05", 2)
        
        #
        # Check that the video is as long as expected.
        #
        self.video.testVideoLength(0, 4.9, 9.0)
        
