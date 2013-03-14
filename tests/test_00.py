#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from tools      import TestUtils
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_clock import *
from apps.app_settings import *
#from datetime 
import datetime

class test_35(GaiaTestCase):
    _Description = "Setting a new alarm (will sleep for a while to give alarm time to start)."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 35)
        self.clock      = AppClock(self)
        self.settings   = AppSettings(self)
                
        #
        # Set timeout for element searches.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Delete all previous alarms.
        #
        if not self.clock.deleteAllAlarms():
            self.UTILS.reportComment("(Couldn't delete previous alarms - problem with external 'gaiatest' script.)")

        #
        # Set the volume to be low (no need to wake up the office! ;o)
        #
        self.settings.setAlarmVolume(1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def _calcStep(self, p_scroller):
        #
        # Calculates how big the step should be
        # when 'flick'ing a scroller (based on the
        # number of elements in the scroller).
        # The idea is to make each step increment
        # the scroller by 1 element.
        #
        x = float(len(p_scroller.find_elements("class name", "picker-unit"))) / 100
        
        #
        # This is a little formula I worked out - seems to work, but it's
        # not perfect (and I've only tested it on the scrollers on my Ungai).
        #
        x = 1 - ((1/(x * 0.8))/100)
        
        return x
        
        
    def _scrollForward(self, p_scroller):
        #
        # Move the scroller forward one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start * x
        
        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)

        time.sleep(0.5)
        
    def _scrollBackward(self, p_scroller):
        #
        # Move the scroller back one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start / x
        
        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)

        time.sleep(0.5)
        
        
    def test_run(self):
        #
        # Launch clock app.
        #
        self.clock.launch()
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.new_alarm_btn"))
        self.marionette.tap(x)

        import time
        time.sleep(2)
        
        p_component = "hours"
        
        scroller = self.UTILS.get_element(
            DOM.Clock.time_picker_column[0], 
            DOM.Clock.time_picker_column[1] % p_component)
        
        self._scrollForward(scroller)
        self._scrollForward(scroller)
        self._scrollForward(scroller)
        self._scrollBackward(scroller)
        self._scrollBackward(scroller)
        self._scrollBackward(scroller)
        
        p_component = "minutes"
        
        scroller = self.UTILS.get_element(
            DOM.Clock.time_picker_column[0], 
            DOM.Clock.time_picker_column[1] % p_component)
        
        self._scrollForward(scroller)
        self._scrollForward(scroller)
        self._scrollForward(scroller)
        self._scrollBackward(scroller)
        self._scrollBackward(scroller)
        self._scrollBackward(scroller)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        