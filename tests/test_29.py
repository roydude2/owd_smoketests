#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests.mock_data.contacts import MockContacts

class test_29(GaiaTestCase):
    _Description = "Killing apps via the homescreen."

    _test_apps = ["Gallery", "FM Radio"]
    _img_list  = ('img1.jpg', 'img2.jpg')
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = AppContacts(self)

        #
        # Load a couple of images into the gallery.
        #
        for i in self._img_list:
            self.UTILS.addFileToDevice('./tests/resources/' + i, destination='DCIM/100MZLLA')
    
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.UTILS.goHome()
        
        #
        # launch the test apps (lifted directly from gaiatest).
        #
        self.test_apps = []
        for app in self._test_apps:
            app1 = app.split(" ")[0].lower()
            test_app = {
                'name'        : app,
                'app'         : self.apps.launch(app),
                'card'        : (DOM.Home.app_card[0], DOM.Home.app_card[1] % app1),
                'close_button': (DOM.Home.app_close[0], DOM.Home.app_close[1] % app1)
            }
            self.test_apps.append(test_app)
            self.UTILS.touchHomeButton()
            time.sleep(1)
        
        self.UTILS.holdHomeButton()
        
        x = self.UTILS.getElement(DOM.Home.cards_view, "App 'cards' list")
        
        #
        # Flick it up (not working currently - retry when marionette toch is working).
        #
#        x = self.UTILS.get_element(*self.test_apps[len(self.test_apps)-1]["card"])
#        els = self.marionette.find_elements(*DOM.Home.app_cards)
#        for x in els:            
#            x_x = int(x.size['width'] / 2)
#            x_y = int(x.size['height'] / 2)
#            self.marionette.flick(x, x_x, x_y, x_x, -100, 1000)
        
        #
        # For now just click the close_button
        #
        self.UTILS.logComment("(Didn't drag the app 'up' to close it, I just clicked the 'close' button.)")
        i = 0
        for app in self._test_apps:
            x = self.UTILS.getElement(self.test_apps[i]["close_button"], "Close button on '" + self.test_apps[i]["name"] + "' card")
            self.marionette.tap(x)

            self.UTILS.waitForNotElements(self.test_apps[i]["card"], "Card for '" + self.test_apps[i]["name"] + "'", True, 5, False)
            i = i + 1

