#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from roytest    import RoyClass1
from gaiatest   import GaiaTestCase


class test_21(GaiaTestCase):
    _Description = "Get an app from the marketplace and run it."
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.ROY      = RoyClass1(self)
        
    def tearDown(self):
        print "FINISHED"
        
    def test_run(self):
        print "STARTING"
        self.ROY.quickTest1()
        
        self.ROY.quickTest2()
        
        self.ROY.quickTest3()
        
        
