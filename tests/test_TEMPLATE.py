#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_??
from gaiatest import GaiaTestCase

class test_?(GaiaTestCase):
    _Description = "Send and receive an SMS via the messaging app."
    
    _TestMsg     = "Smoke test 10 sms - reply with this same message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.testUtils  = TestUtils(self, ?)
        self.??   = app_??.main(self, self.testUtils)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Establish parameters.
        #
        self.MYVAR = self.testUtils.get_os_variable("MY_VAR", "Something about MY_VAR")
        self.testUtils.reportComment("Using " + self.MYVAR)
        
    def tearDown(self):
        self.testUtils.reportResults()
        
    def test_run(self):
        
        #
        # Launch ?? app.
        #
        self.??.launch()


