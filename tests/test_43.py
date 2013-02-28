import sys
sys.path.insert(1, "./")

from tools import TestUtils
from tests.shared_test_functions import FTU_LANG_KB
from gaiatest import GaiaTestCase

class test_42(GaiaTestCase):
    _Description = "First time use screens - check PORTUGUESE keyboard."
    
    _LANG           = "Portuguese (Brazil)"
    _SCREEN_SIZES   = (45132, 21224, 21359, 20615)
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS   = TestUtils(self, 42)
        self.FTU_KB  = FTU_LANG_KB.main(self, self._LANG, self._SCREEN_SIZES)
        
    def tearDown(self):
        self.UTILS.reportResults()
    
    def test_run(self):
        self.FTU_KB.run()

