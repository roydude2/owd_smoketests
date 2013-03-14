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
import datetime, time   

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

        #        
        # Make sure the date and timezone are correct before setting alarms.
        #
#        self.data_layer.set_setting('time.timezone', 'Europe/Madrid')
#        self.data_layer.set_time(20130314133200)


    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        return
        #
        # Launch clock app.
        #
        self.clock.launch()
        
        #
        # Create an alarm that is 1 minute in the future.
        #
        _mins_to_wait = 1
        
        # (Make sure we're not about to do this at the end of a minute.)
        import time
        now_secs = time.time() / 60
        if now_secs > 45:
            time.sleep(16)
        
        t = datetime.datetime.now() + datetime.timedelta(minutes=_mins_to_wait)
        
        _hour   = t.hour
        _minute = t.minute
        _title  = "Test 35 alarm"

        self.clock.createAlarm(_hour, _minute, _title)

        #
        # Return to the main screen (since this is where the user will
        # most likely be when the alarm goes off).
        #
        self.UTILS.goHome()
        
        #
        # Check the statusbar icon exists.
        #
        self.UTILS.TEST(self.clock.checkStatusbarIcon(), "Alarm icon not present in statusbar.")

        #
        # Wait for the alarm to start.
        #
        self.clock.checkAlarmDetails(_hour, _minute, _title)
