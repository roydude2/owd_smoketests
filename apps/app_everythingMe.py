import DOM, time
from gaiatest   import GaiaTestCase
from utils      import UTILS
from marionette import Marionette

class AppEverythingMe(GaiaTestCase):
    
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
        #
        # Go to the homescreen.
        #
        self.UTILS.goHome()
        
        #
        # Scroll to the left to expose the 'everything.me' screen.
        #
        self.UTILS.scrollHomescreenLeft()
        self.UTILS.waitForElements(DOM.EME.groups, "EME group list", True, 30)

    def pickGroup(self, p_name):
        #
        # Pick a group from the main icons.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "EME group list")
        for groupLink in x:
            if groupLink.get_attribute("data-query") == p_name:
                self.marionette.tap(groupLink)
                return True
        
        return False
        

    def addAppToHomescreen(self, p_name):
        #
        # Pick an app from the apps listed in this group.
        #
        x = self.UTILS.getElements(DOM.EME.apps, "Apps list")
        for appLink in x:
            if appLink.get_attribute("data-name") == p_name:
                self.marionette.long_press(appLink)
                self.marionette.switch_to_frame()
                x = self.UTILS.getElement(DOM.EME.add_app_to_homescreen, "Add app to homescreen button")
                self.marionette.tap(x)
                
                # This isn't obvious, but you need to scroll the screen right
                # to reset the position for finding the app later, so I'm
                # doing it here.
                time.sleep(2)
                self.UTILS.goHome()
                self.UTILS.scrollHomescreenRight()

                return True
        
        return False

