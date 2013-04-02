import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppCamera(GaiaTestCase):
    
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

        
        #
        # Default to not prompting for geolocation (this was broken in Gaia recently so 'try' it).
        #
        try:
            self.apps.set_permission('Camera', 'geolocation', 'deny')
        except:
            self.UTILS.logComment("Couldn't automatically set Camera geolocation permission!")
        

    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Camera')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");
        
    def switchSource(self):
        switchBTN = self.UTILS.getElement(DOM.Camera.switch_source_btn, "Source switcher")
        self.marionette.tap(switchBTN)
        self.UTILS.waitForElements(DOM.Camera.capture_button_enabled, "Enabled capture button")

    #
    # Take a picture.
    #
    def takePicture(self):
        x = self.UTILS.getElement(DOM.Camera.capture_button, "Capture button")
        self.marionette.tap(x)
        self.UTILS.waitForElements(DOM.Camera.thumbnail, "Camera thumbnails")
        
    #
    # Click thumbnail.
    #
    def clickThumbnail(self, p_num):
        thumbEls = self.UTILS.getElements(DOM.Camera.thumbnail, "Camera thumbnails")
        myThumb = thumbEls[p_num]
        self.marionette.tap(myThumb)

    #
    # Check the length of a video.
    #
    def checkVideoLength(self, p_vid_num, p_from_SS, p_to_SS):
            
        #
        # Find the thumbnail for this video and click it.
        #
        self.clickThumbnail(p_vid_num)
        
        #
        # Click the button to play the video and make sure it takes between
        # 5 and 9 seconds to complete (to allow time delay in element
        # loading).
        #
        playBTN = self.UTILS.getElement(DOM.Camera.video_play_button, "Video play button")
        self.marionette.tap(playBTN)

        # Start the timer when the pause button is visible.
        self.UTILS.waitForElements(DOM.Camera.video_pause_button, 
                                   "Video pause button", True, 20, False)
        start_time = time.time()
        
        # Stop the timer when the pause button is no longer visible.
        self.UTILS.waitForNotElements(DOM.Camera.video_pause_button, 
                                      "Video pause button", True, 20, False);
        
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)

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
        captureBTN = self.UTILS.getElement(DOM.Camera.capture_button, "Capture button")
        self.marionette.tap(captureBTN)
        
        # Record for 5 seconds
        try:
            self.wait_for_condition(lambda m: m.find_element(*DOM.Camera.video_timer).text == p_length_str_MMSS)
        except:
            self.UTILS.logResult(False, "Video timer never reached " + p_length_str_MMSS + ".")
            
        # Stop recording
        self.marionette.tap(captureBTN)

        self.UTILS.waitForNotElements(DOM.Camera.video_timer, "Video timer", True, 20, False);

        self.UTILS.waitForElements(DOM.Camera.thumbnail, 
                                    "Thumbnail appears after recording video", True, 20, False)
        
        # TEST: Thumbnail has not been previewed yet.
        prev_marker = self.UTILS.getElement(DOM.Camera.thumbnail_preview_marker, "Thumbnail preview marker", False)
        self.UTILS.TEST((prev_marker.get_attribute("class") == "offscreen"), "Image is not previewed as soon as picture is taken.")
        
