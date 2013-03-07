from apps import DOM
from gaiatest import GaiaTestCase
from tools import TestUtils
import time

class main(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.marionette = p_parent.marionette
#        self.UTILS      = p_parent.UTILS
        self.apps       = p_parent.apps
        
        self.UTILS      = TestUtils(p_parent, 00)

    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Calendar')
        self.wait_for_element_not_displayed(*DOM.GLOBAL.loading_overlay)

    def addEvent(self):
        x = self.UTILS.get_element(*DOM.Calendar.add_event_btn)
        self.marionette.tap(x)
        
    #
    # Create a new event - use 'False' in the following fields if you want to leave them at default:
    #
    #   start date
    #   end date
    #   location
    #   notes
    #
    def createEvent(self, p_title, p_location, p_allDay, p_startDate, p_startTime, p_endDate, p_endTime, p_notes):
        self.addEvent()
        
        #
        # Set the title.
        #
        x = self.UTILS.get_element(*DOM.Calendar.event_title)
        x.send_keys(p_title)

        #
        # Set the location.
        #
        if p_location:
            x = self.UTILS.get_element(*DOM.Calendar.event_location)
            x.send_keys(p_location)

        #
        # Set the 'all day' marker.
        #
        if p_allDay:
            x = self.UTILS.get_element(*DOM.Calendar.event_allDay)
            self.marionette.tap(x)

        #
        # Set start date.
        #
        if p_startDate: 
            x = self.UTILS.get_element(*DOM.Calendar.event_start_date)
            x.send_keys(p_startDate)
        
        #
        # Start start time.
        #
        x = self.UTILS.get_element(*DOM.Calendar.event_start_time)
        x.send_keys(p_startTime)
        
        #
        # Set end date.
        #
        if p_endDate: 
            x = self.UTILS.get_element(*DOM.Calendar.event_end_date)
            x.send_keys(p_endDate)
        
        #
        # Set end time.
        #
        x = self.UTILS.get_element(*DOM.Calendar.event_end_time)
        x.send_keys(p_endTime)
        
        #
        # Set notes.
        #
        if p_notes: 
            x = self.UTILS.get_element(*DOM.Calendar.event_notes)
            x.send_keys(p_notes)
        
        #
        # Save it.
        #
        x = self.UTILS.get_element(*DOM.Calendar.event_save_btn)
        self.marionette.tap(x)
        
    #
    # Set to view type (day / week / month).
    #
    def setView(self, p_type):
        x = self.UTILS.get_element(DOM.Calendar.view_type[0], DOM.Calendar.view_type[1] % p_type)
        self.marionette.tap(x)
        
    #
    # Return object for an event in month view.
    #
    def getEventPreview(self, p_view, p_hour24, p_title, p_location=False):
        
        #
        # The tag identifiers aren't consistent, so set them here.
        #
        # <type>: (<event preview identifier>, <event title identifier>)
        #
        event_view = {
            "month": (DOM.Calendar.view_events_block_m % p_hour24, DOM.Calendar.view_events_title_month),
            "week" : (DOM.Calendar.view_events_block_w % p_hour24, DOM.Calendar.view_events_title_week),
            "day"  : (DOM.Calendar.view_events_block_d % p_hour24, DOM.Calendar.view_events_title_day)
        }
        
        viewStr = event_view[p_view]
        
        #
        # Switch to the desired view.
        #
        # For the life of me I can't get 'wait_for_element' ... to work in day view, so I'm
        # just waiting a few seconds then checking with .is_displayed() instead.
        #
        self.setView(p_view)
        time.sleep(2)
        
        try:
            #
            # Start by getting the parent element objects, which could contain event details.
            #
            event_objects = self.marionette.find_elements('xpath', viewStr[0])
        except:
            self.UTILS.reportError("Couldn't find ANY events for hour " + p_hour24 + " in " + p_view + " view.")
            return False
        else:
            for event_object in event_objects:
                if event_object.is_displayed():
                    #
                    # This parent element is visible, so check the title component.
                    #
                    try:
                        ev_title = event_object.find_element('xpath', viewStr[1] % p_title)
                    except:
                        pass
                    else:
                        # ... and location (if specifed and if this isn't 'week' view).
                        #
                        if p_location and (p_view != "week"):
                            # (the location string is only present for day + month, and IS consistent)
                            try:
                                ev_locat = event_object.find_element(
                                    'xpath',
                                    DOM.Calendar.view_events_locat % p_location)
                            except:
                                pass
                            else:
                                return event_object
                        else:
                            return event_object
        
        #
        # If we get to here we failed to return the element we're after.
        #
        return False
                    