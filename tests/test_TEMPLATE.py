#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from tools      import TestUtils
from gaiatest   import GaiaTestCase
import DOM

#
# Imports particular to this test case.
#
from apps.app_gallery import *

class test_??(GaiaTestCase):
    _Description = "??"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self)
        self.gallery    = AppGallery(self)
        
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


