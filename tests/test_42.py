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
from tests.shared_test_functions import FTU_LANG_KB

class test_42(GaiaTestCase):
    _Description = "First time use screens - check ENGLISH keyboard."
    
    _LANG           = "English (US)"
#    _SCREEN_SIZES   = (45132, 21224, 21359, 20615)
#    _SCREEN_SIZES   = (45132, 21285, 20594, 20641)
    _SCREEN_SIZES   = (44017, 21285, 20594, 20641)
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS   = TestUtils(self)
        self.FTU_KB  = FTU_LANG_KB.main(self, self._LANG, self._SCREEN_SIZES)
        
    def tearDown(self):
        self.UTILS.reportResults()
    
    def test_run(self):
        self.FTU_KB.run()

