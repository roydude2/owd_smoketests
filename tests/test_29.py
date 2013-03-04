import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_contacts
from tests.mock_data.contacts import MockContacts
from gaiatest import GaiaTestCase
import time

class test_29(GaiaTestCase):
    _Description = "Create a contact via the contacts app."

    _test_apps = ["Gallery", "FM Radio"]
    _img_list  = ('img1.jpg', 'img2.jpg')
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = TestUtils(self, 29)
        self.contacts  = app_contacts.main(self, self.UTILS)

        #
        # Load a couple of images into the gallery.
        #
        for i in self._img_list:
            self.push_resource(i, destination='DCIM/100MZLLA')
    
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
        
        x = self.UTILS.get_element(*DOM.Home.cards_view)
        self.UTILS.TEST(x.is_displayed(), "Currently running apps not displayed as expected.", True)
        
        #
        # Flick it up (not working currently - retry when marionette toch is working).
        #
        #x = self.UTILS.get_element(*self.test_apps[0]["card"])
        #x_x = int(x.size['width'] / 2)
        #x_y = int(x.size['height'] / 2)
        #self.marionette.flick(x, x_x, x_y, x_x, 0, 1000)
        
        #
        # For now just click the close_button
        #
        i = 0
        for app in self._test_apps:
            x = self.UTILS.get_element(*self.test_apps[i]["close_button"])
            self.marionette.tap(x)
            time.sleep(1)
            i = i + 1

