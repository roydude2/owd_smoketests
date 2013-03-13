import DOM, time
from gaiatest   import GaiaTestCase
from tools      import TestUtils
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
        self.UTILS      = TestUtils(self, 00)        
        if True:
            self.marionette = p_parent.marionette
            self.UTILS      = p_parent.UTILS



    def launch(self):
        #
        # Go to the homescreen.
        #
        self.UTILS.goHome()
        time.sleep(2)
        
        #
        # Scroll to the left to expose the 'everything.me' screen.
        #
        x = self.marionette.find_element(*self.UTILS.verify("DOM.EME.here_check"))
        while not x.is_displayed():
            self.UTILS.scrollHomescreenLeft()

        try:
            x = self.UTILS.get_elements(*self.UTILS.verify("DOM.EME.icons_groups"))
            if len(x) > 0:
                return True
            else:
                return False
        except:
            return False

    #
    # Pick a group from the main icons.
    #
    def pickGroup(self, p_num):
        x = self.UTILS.get_elements(*self.UTILS.verify("DOM.EME.icons_groups"))
        self.marionette.tap(x[p_num])

    #
    # Pick an app from the apps listed.
    # Since the app names aren't present in the html I have to depend on
    # a unique id number.
    #
    def addAppToHomescreen(self, p_num):
        x = self.UTILS.get_element('id', p_num)
        self.marionette.long_press(x)
        self.marionette.switch_to_frame()
        x = self.UTILS.get_element(*self.UTILS.verify("DOM.EME.add_app_to_homescreen"))
        self.marionette.tap(x)

