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
        
    def test_run(self):
        #
        # Launch clock app.
        #
        self.clock.launch()
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.new_alarm_btn"))
        self.marionette.tap(x)
        
        
        t = datetime.datetime.now() + datetime.timedelta(minutes=3)
        
        _hour   = t.hour
        _minute = t.minute
        _title  = "Test 35 alarm"

        #
        # Sort the time out into 12 hour format.
        #
        x = self.clock.switch_24_12(_hour)
        t_hour = x[0]
        t_ampm = x[1]

        #
        # Set the hour.
        #
        self.clock._select("hours", t_hour)
        
        
        scroller = self.UTILS.get_element(
            DOM.Clock.time_picker_column[0], 
            DOM.Clock.time_picker_column[1] % "hours")
        
        self.clock._scrollForward(scroller)
        self.clock._scrollForward(scroller)
        self.clock._scrollForward(scroller)
        import time
        time.sleep(2)
        self.clock._scrollBackward(scroller)
        self.clock._scrollBackward(scroller)
        self.clock._scrollBackward(scroller)
        
        
        
        
        
