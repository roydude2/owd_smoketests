#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_email
from gaiatest import GaiaTestCase

class test_?(GaiaTestCase):
    _Description = "?????"
    
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, ?)
        self.??     = app_??.main(self, self.UTILS)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
        #
        # Establish parameters.
        #
        self.MYVAR = self.UTILS.get_os_variable("MY_VAR", "Something about MY_VAR")
        self.UTILS.reportComment("Using " + self.MYVAR)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch ?? app.
        #
        self.??.launch()


