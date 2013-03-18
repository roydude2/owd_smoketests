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
from apps.app_ftu import *

class test_27(GaiaTestCase):
    _Description = "First time use screens."
    
    _boolCheck   = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = TestUtils(self, 27)
        self.FTU        = AppFTU(self)
        self.wifi_name  = self.UTILS.get_os_variable("WIFI_TEST_27", "Name of wifi to connect to (case sensitive!)")
        self.wifi_user  = self.UTILS.get_os_variable("USERNAME_27", "Wifi username")
        self.wifi_pass  = self.UTILS.get_os_variable("PASSWORD_27", "Wifi password")

        #
        # These are the choices we want just now, so just hardcode them.
        #
        #self.continent  = self.UTILS.get_os_variable("CONTINENT_27", "Continent for timezone")
        #self.city       = self.UTILS.get_os_variable("CITY_27", "City for timezone")
        #self.language   = self.UTILS.get_os_variable("LANG_27", "Language for device")
        self.continent = "Europe"
        self.city      = "Madrid"
        self.language  = "English (US)"
        
        self.UTILS.reportComment("Using wifi name: " + self.wifi_name)
        self.UTILS.reportComment("Using wifi user: " + self.wifi_user)
        self.UTILS.reportComment("Using wifi pass: " + self.wifi_pass)
        self.UTILS.reportComment("Using continent: " + self.continent)
        self.UTILS.reportComment("Using city     : " + self.city)
        self.UTILS.reportComment("Using language : " + self.language)
        
        #
        # Turn off wifi and dataconn.
        #
        self.data_layer.disable_wifi()
        self.data_layer.disable_cell_data()
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch FTU app.
        #
        self.FTU.launch()

        #
        # LANGUAGE.
        #
        self.FTU.setLanguage(self.language)
        self.FTU.nextScreen()
        
        #
        # DATA CONNECTIVITY.
        #
        self.FTU.setDataConnEnabled()
        self.FTU.nextScreen()
        
        #
        # WIFI CONNECTIVITY.
        #
#        self.FTU.setNetwork(self.wifi_name, self.wifi_user, self.wifi_pass)
        self.FTU.nextScreen()
        
        #
        # TIMEZONE.
        #
        self.FTU.setTimezone(self.continent, self.city)

        #
        # Skip the import contacts / privacy / etc... screens until you get to the Tour.
        #
        tourStartBtn = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.tour_start_btn"))

        while not tourStartBtn.is_displayed():
            self.FTU.nextScreen()
        
        #
        # TOUR.
        #
        self.FTU.startTour()
        
        #
        # Move through the tour until we hit the end.
        #
        tourEndBtn = self.marionette.find_element(*self.UTILS.verify("DOM.FTU.tour_finished_btn"))
        
        while not tourEndBtn.is_displayed():
            self.FTU.nextTourScreen()
            
        self.FTU.endTour()
