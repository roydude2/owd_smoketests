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
        # Set the volume to be low (no need to wake up the office! ;o)
        #
        self.settings.setAlarmVolume(1)

        #        
        # Make sure the date and timezone are correct before setting alarms.
        #
        _continent  = self.UTILS.get_os_variable("YOUR_CONTINENT", "YOUR continent (for setting timezone).")
        _city       = self.UTILS.get_os_variable("YOUR_CITY", "YOUR city (for setting timezone).")
        self.data_layer.set_setting('time.timezone', _continent + "/" + _city)
        self.UTILS.setTimeToNow()


    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
    
        #
        # Launch clock app.
        #
        self.clock.launch()
        
        #
        # Delete all previous alarms.
        #
        #
        self.clock.deleteAllAlarms() 

        #
        # Create an alarm that is 1 minute in the future.
        #
        # (Make sure we're not about to do this at the end of a minute or an hour.)
        #
        now_mins = time.strftime("%M", time.gmtime())
        diff_m   = 60 - int(now_mins)
        if diff_m <= 1:
            time.sleep(60)
        
        now_secs = time.strftime("%S", time.gmtime())
        diff_s   = 60 - int(now_secs)
        if diff_s <= 15:
            time.sleep(diff_s)


        t = datetime.datetime.now() + datetime.timedelta(minutes=1)
        
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
