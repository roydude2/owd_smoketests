import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_clock, app_settings
from gaiatest import GaiaTestCase
import datetime


class test_35(GaiaTestCase):
    _Description = "Setting a new alarm (will sleep for a while to give alarm time to start)."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 35)
        self.clock      = app_clock.main(self, self.UTILS)
        self.settings   = app_settings.main(self, self.UTILS)
                
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
        
        #
        # Create an alarm that is 2 minutes in the future.
        #
        _mins_to_wait = 2
        t = datetime.datetime.now() + datetime.timedelta(minutes=_mins_to_wait)
        
        _hour   = t.hour
        _minute = t.minute
        _title  = "Test 35 alarm"

        self.clock.newAlarm(_hour, _minute, _title)
        
        #
        # Go home and wait for the alarm.
        #
        self.UTILS.goHome()
        
        # (Because the notifier always seems to be classed as 'visible', we have to manually wait.)
        import time
        time.sleep(_mins_to_wait * 60)
        
        self.clock.checkAlarmDetails(_hour, _minute, _title)
