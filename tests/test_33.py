#
# This is a template for new tests - make the required changes - refer to previous tests if you need help.
#
import sys
sys.path.insert(1, "./")

from tools import TestUtils
from apps import DOM, app_calculator
from gaiatest import GaiaTestCase

class test_33(GaiaTestCase):
    _Description = "Basic calculator test."
    
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS  = TestUtils(self, 33)
        self.Calc   = app_calculator.main(self, self.UTILS)
        
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch calculator app.
        #
        self.Calc.launch()

        btn3 = self.UTILS.get_element(*DOM.Calculator.button_3)
        self.marionette.tap(btn3)
        
        btnX = self.UTILS.get_element(*DOM.Calculator.button_mutiply)
        self.marionette.tap(btnX)
        
        btn5 = self.UTILS.get_element(*DOM.Calculator.button_5)
        self.marionette.tap(btn5)
        
        btnEQ = self.UTILS.get_element(*DOM.Calculator.button_equals)
        self.marionette.tap(btnEQ)
        
        Answer = self.UTILS.get_element(*DOM.Calculator.display)
        
        self.UTILS.TEST(Answer.text == "15", "Expected answer to be 15, but it was " + Answer.text + ".")
        
