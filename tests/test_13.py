#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_13(GaiaTestCase):
    _Description = "Play recorded video in the video player app."
    
    def setUp(self):
        #
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.camera     = AppCamera(self)
        self.video      = AppVideo(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
    
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordVideo("00:05")
        self.camera.checkVideoLength(0, 4.9, 10.1)

        #
        # Open the video player application.
        #
        self.apps.kill_all()
        self.video.launch()
        time.sleep(5)
        
        #
        # the first thumbnail should be our video.
        #
        self.video.checkThumbDuration(0, "00:05", 2)
        
        #
        # Check that the video is as long as expected.
        #
        self.video.checkVideoLength(0, 4.9, 10.1)
        
