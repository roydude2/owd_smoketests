from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    def setTimeToNow(self):
        #
        # Set the phone's time (using gaia data_layer instead of the UI).
        #
        self.parent.data_layer.set_time(time.time() * 1000)
        
    def get_os_variable(self, p_name, p_msg=False):
        #
        # Get a variable from the OS.
        #
        if p_name == "ENTER":
            return ""
        else:
            return os.environ[p_name]
    