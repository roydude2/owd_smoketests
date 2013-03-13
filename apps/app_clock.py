import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
from marionette import Marionette

class AppClock(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = TestUtils(self, 00)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS



    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Clock')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    def deleteAllAlarms(self):
        try:
            self.data_layer.delete_all_alarms()
            return True
        except:
            return False
        
    #
    # Takes an hour and returns array "hour" (12 hour format) and "ampm".
    #
    def switch_24_12(self, p_hour):
        if p_hour >= 12:
            t_ampm = "PM"
            if p_hour > 12:
                t_hour = p_hour - 12
            else:
                t_hour = p_hour
        else:
            t_hour = p_hour
            t_ampm = "AM"
        
        return (t_hour, t_ampm)
        
    #
    # Create a new alarm.
    #
    def createAlarm(self, p_hour, p_min, p_label, p_repeat="Never", p_sound="Classic Buzz", p_snooze="5 minutes"):
        #
        # Click the new alarm button.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.new_alarm_btn"))
        self.marionette.tap(x)
        
        #
        # Sort the time out into 12 hour format.
        #
        x = self.switch_24_12(p_hour)
        t_hour = x[0]
        t_ampm = x[1]

        self.UTILS.reportComment("Creating new alarm for " + str(t_hour) + ":" + str(p_min).zfill(2) + " " + t_ampm)
        
        #
        # Set the hour.
        #
        self._select("hours", t_hour)
        
        #
        # Set the minutes.
        #
        self._select("minutes", p_min)
        
        #
        # Set the AM / PM.
        #
        scroller = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.time_picker_ampm"))
        currVal  = scroller.find_element(*self.UTILS.verify("DOM.Clock.time_picker_curr_val")).text
        
        if t_ampm != currVal:
            if currVal == "AM":
                self._scrollForward(scroller)
            else:
                self._scrollBackward(scroller)
                
        #
        # Set the label.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.alarm_label"))
        x.send_keys(p_label)
        
        #
        # TODO: Set the repeat, sound and snooze.
        #
        
        #
        # Save the alarm.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.alarm_done"))
        self.marionette.tap(x)
        
        #
        # Check the alarm details are displayed in the clock screen.
        #
        self.checkAlarmPreview(t_hour, p_min, t_ampm, p_label, p_repeat)
        
    #
    # Verify the alarm details in the clock screen.
    #
    def checkAlarmPreview(self, p_hour, p_min, p_ampm, p_label, p_repeat):
        #
        # Make sure we're looking at the clock face.
        #
        self.launch()
        
        # Put the time in a format we can compare easily with.
        p_time = str(p_hour) + ":" + str(p_min).zfill(2)
        
        alarms = self.UTILS.get_elements(*self.UTILS.verify("DOM.Clock.alarm_preview_alarms"))
        
        foundBool = False
        for alarm in alarms:
            alarm_time   = alarm.find_element(*self.UTILS.verify("DOM.Clock.alarm_preview_time")).text
            alarm_ampm   = alarm.find_element(*self.UTILS.verify("DOM.Clock.alarm_preview_ampm")).text
            alarm_label  = alarm.find_element(*self.UTILS.verify("DOM.Clock.alarm_preview_label")).text
            alarm_repeat = alarm.find_element(*self.UTILS.verify("DOM.Clock.alarm_preview_repeat")).text
            
            if  p_time      == alarm_time   and \
                p_ampm      == alarm_ampm   and \
                p_label     == alarm_label  and \
                p_repeat    == alarm_repeat:
                    foundBool = True
                    break
        
        self.UTILS.TEST(foundBool, "Alarm details not displayed correctly on the Clock screen.")
             
             
    def checkStatusbarIcon(self):
        #
        # Check for the little alarm bell icon in the statusbar of the
        # homescreen.
        #
        self.marionette.switch_to_frame()
        boolOK = True
        try:
            self.wait_for_element_displayed(*DOM.Clock.alarm_notifier)
        except:
            boolOK = False
        
        return boolOK
                
    #
    # Check details of alarm when it rings.
    #
    # NOTE: the status bar alarm is always 'visible', so you have to manually
    #       wait until the alarm is expected to have started before calling this!
    #
    def checkAlarmDetails(self, p_hour, p_min, p_label):

        #
        # The alarm screen appears in a different frame to the clock.
        # Try to access this frame a few times to give the alarm time to appear.
        #
        self.marionette.switch_to_frame()
        
        retries = 40
        while retries >= 0:
            retries = retries - 1
            try:
                self.UTILS.switchToFrame(*DOM.Clock.alarm_alert_iframe)
                break
            except:
                time.sleep(3)
            
        
        #
        # Sort the time out into 12 hour format.
        #
        x = self.switch_24_12(p_hour)
        t_hour = x[0]
        t_ampm = x[1]

        # Put the time in a format we can compare easily with.
        p_time = str(t_hour) + ":" + str(p_min).zfill(2)
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.alarm_alert_time")).text
        self.UTILS.TEST(x == p_time, "Incorrect time shown when alarm is ringing: expected '" + p_time + "', but it was '" + x + "'.")
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.alarm_alert_ampm")).text
        self.UTILS.TEST(x == t_ampm, "Incorrect AM / PM shown when alarm is ringing: expected '" + t_ampm + "', but it was '" + x + "'.")
        
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.alarm_alert_label")).text
        self.UTILS.TEST(x == p_label, "Incorrect label shown when alarm is ringing: expected '" + p_label + "', but it was '" + x + "'.")
        
        #
        # Stop the alarm.
        #
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.Clock.alarm_alert_close"))
        self.marionette.tap(x)

    #
    # Scroll forward and backward.
    #
    def _scrollForward(self, p_scroller):
#        #
#        # Start in the middle and flick to 'almost' the top.
#        #
#        x_pos   = p_scroller.size['width']  / 2
#        y_start = p_scroller.size['height'] / 2
#        y_end   = y_start * 0.87
#        self.UTILS.reportComment("(" + \
#                                 str(x_pos) + ", " + \
#                                 str(y_start) + ", " + \
#                                 str(x_pos) + ", " + \
#                                 str(y_end) + ", " + \
#                                 "300)")
##        x_pos   = "%.0f" % x_pos
##        y_start = "%.0f" % y_start
##        y_end   = "%.0f" % y_end
##        self.UTILS.reportComment("(" + \
##                                 str(x_pos) + ", " + \
##                                 str(y_start) + ", " + \
##                                 str(x_pos) + ", " + \
##                                 str(y_end) + ", " + \
##                                 "300)")
#        
        
#        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 300)
        self.marionette.flick(p_scroller, 50, 100, 50, 63, 300)

        time.sleep(1)
        
    def _scrollBackward(self, p_scroller):
        self.marionette.flick(p_scroller, 50, 63, 50, 100, 300)
        time.sleep(1)
        
    #
    # Set the time using the scroller.
    # Marionette flick() works a treat here, woop!
    #
    def _select(self, p_component, p_number):
        scroller = self.UTILS.get_element(
            DOM.Clock.time_picker_column[0], 
            DOM.Clock.time_picker_column[1] % p_component)
        
        #
        # Get the current setting for this scroller.
        #
        currVal = scroller.find_element(*self.UTILS.verify("DOM.Clock.time_picker_curr_val")).text
        
        #
        # Now flick the scroller as many times as required 
        # (the current value might be padded with 0's so check for that match too).
        #
        while str(p_number) != currVal and str(p_number).zfill(2) != currVal:
            # Do we need to go forwards or backwards?
            if p_number > int(currVal):
                self._scrollForward(scroller)
            if p_number < int(currVal):
                self._scrollBackward(scroller)
                
            # Get the new 'currVal'.
            currVal = scroller.find_element(*self.UTILS.verify("DOM.Clock.time_picker_curr_val")).text
                

