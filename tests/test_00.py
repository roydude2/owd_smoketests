import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_messages
from gaiatest import GaiaTestCase
import os, time

class test_00(GaiaTestCase):
    _Description = "(Just a place to work things out :)"
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.testUtils = TestUtils(self, 00)
        self.MYAPP   = app_messages.main(self, self.testUtils)

        self.marionette.set_search_timeout(50)
            
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Open the gallery application.
        #
        z = './/*[@id="desktop-notifications-container"]//div[contains(text(), "628842372")]'
        
        x=(DOM.Messages.statusbar_new_sms[0], z)
        
        #
        # Wait for the notification to be present for this number (3 minute timeout)
        # in the popup messages (this way we make sure it's coming from our number,
        # as opposed to just containing our number in the notification).
        #
        x = self.testUtils.waitForStatusBarNew(x, 2)
        
        self.testUtils.savePageHTML("/tmp/roy1.html")
        
        self.testUtils.TEST(x, "BOO!")
