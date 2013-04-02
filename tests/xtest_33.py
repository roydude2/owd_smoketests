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
from apps.app_calculator import *

class test_33(GaiaTestCase):
    _Description = "Basic calculator test."
    
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self)
        self.Calc   = AppCalculator(self)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch calculator app.
        #
        self.Calc.launch()
        
        btn3 = self.UTILS.get_element(DOM.Calculator.button_3, "Calculator button 3")
        self.marionette.tap(btn3)
        
        btnX = self.UTILS.get_element(DOM.Calculator.button_mutiply, "Calculator button X")
        self.marionette.tap(btnX)
        
        btn5 = self.UTILS.get_element(DOM.Calculator.button_5, "Calculator button 5")
        self.marionette.tap(btn5)
        
        btnEQ = self.UTILS.get_element(DOM.Calculator.button_equals, "Calculator button =")
        self.marionette.tap(btnEQ)
        
        Answer = self.UTILS.get_element(DOM.Calculator.display, "Calculator display")
        
        self.UTILS.TEST(Answer.text == "15", "Answer is 15 (it was " + Answer.text + ").")
        
        