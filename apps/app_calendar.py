import DOM, time
from gaiatest   import GaiaTestCase
from utils      import UTILS
from marionette import Marionette

class AppCalendar(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer

        # Just so I get 'autocomplete' in my IDE!
        self.marionette = Marionette()
        self.UTILS      = UTILS(self)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS


    def launch(self):
        self.apps.kill_all()
        self.app = self.apps.launch('Calendar')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Loading overlay");

    def addEvent(self):
        #
        # Press the 'add event' button.
        #
        x = self.UTILS.getElement(DOM.Calendar.add_event_btn, "Add event button")
        self.marionette.tap(x)
        
    def createEvent(self, p_title, p_location, p_allDay, p_startDate, p_startTime, p_endDate, p_endTime, p_notes):
        self.addEvent()
        #
        # Create a new event - use 'False' in the following fields if you want to leave them at default:
        #
        #   start date
        #   end date
        #   location
        #   notes
        #
        
        #
        # Set the title.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_title, "'Title' field")
        x.send_keys(p_title)

        #
        # Set the location.
        #
        if p_location:
            x = self.UTILS.getElement(DOM.Calendar.event_location, "'Location' field")
            x.send_keys(p_location)

        #
        # Set the 'all day' marker.
        #
        if p_allDay:
            x = self.UTILS.getElement(DOM.Calendar.event_allDay, "All day marker")
            self.marionette.tap(x)

        #
        # Set start date.
        #
        if p_startDate: 
            x = self.UTILS.getElement(DOM.Calendar.event_start_date, "'Start date' field")
            x.send_keys(p_startDate)
        
        #
        # Start start time.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_start_time, "'Start time' field")
        x.send_keys(p_startTime)
        
        #
        # Set end date.
        #
        if p_endDate: 
            x = self.UTILS.getElement(DOM.Calendar.event_end_date, "'End date' field")
            x.send_keys(p_endDate)
        
        #
        # Set end time.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_end_time, "'End time' field")
        x.send_keys(p_endTime)
        
        #
        # Set notes.
        #
        if p_notes: 
            x = self.UTILS.getElement(DOM.Calendar.event_notes, "'Notes' field")
            x.send_keys(p_notes)
        
        #
        # Save it.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_save_btn, "Save button")
        self.marionette.tap(x)
        
    def setView(self, p_type):
        #
        # Set to view type (day / week / month).
        #
        x = self.UTILS.getElement((DOM.Calendar.view_type[0], DOM.Calendar.view_type[1] % p_type),
                                  "'" + p_type + "' view type selector")
        self.marionette.tap(x)
        
    def getEventPreview(self, p_view, p_hour24, p_title, p_location=False):
        #
        # Return object for an event in month / week or day view.
        #
        
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
        
        #
        # Start by getting the parent element objects, which could contain event details.
        #
        event_objects = self.UTILS.getElements(('xpath', viewStr[0]), "Event details list", False, 20, False)
        if len(event_objects) <= 0:
            return False

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
                    
