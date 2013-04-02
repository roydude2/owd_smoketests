from global_imports import *

import app_utilities        , \
       debug_utilities      , \
       element_utilities    , \
       general_utilities    , \
       home_utilities       , \
       iframe_utilities     , \
       reporting_utilities  , \
       statusbar_utilities  , \
       test_utilities
       

class TestUtils(app_utilities.main        ,
                debug_utilities.main      ,
                element_utilities.main    ,
                general_utilities.main    ,
                home_utilities.main       ,
                iframe_utilities.main     ,
                reporting_utilities.main  ,
                statusbar_utilities.main  ,
                test_utilities.main):
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.parent         = p_parent
        self.apps           = p_parent.apps
        self.marionette     = p_parent.marionette
        self._resultArray   = []
        self._commentArray  = []
        self.errNum         = 0
        self.passed         = 0
        self.failed         = 0
        self.start_time     = time.time()

        self.testNum        = self.get_os_variable("TEST_NUM")
        self.testDesc       = self.get_os_variable("TEST_DESC")
        self.det_fnam       = self.get_os_variable("DET_FILE")
        self.sum_fnam       = self.get_os_variable("SUM_FILE")
        
