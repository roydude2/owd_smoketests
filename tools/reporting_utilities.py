from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):

    def logResult(self, p_result, p_msg, p_fnam=False):
        #
        # Add a test result to the result array.
        #
        logMsg = p_msg
        
        #
        # The double brackets is intentional (add a 2 part
        # array: true/false + message).
        #
        self._resultArray.append((p_result, logMsg))
        
        if p_fnam:
            self._resultArray.append(("info", "  |__ [current html source = " + p_fnam[0] + "]"))
            self._resultArray.append(("info", "  |__ [current screenshot  = " + p_fnam[1] + "]"))

    
    def logComment(self, p_str):
        #
        # Add a comment to the comment array.
        #
        self._commentArray.append(p_str)

    def reportResults(self):
        #
        # Create the final result file from the result and comment arrays
        # (run only once, at the end of each test case).
        #

        #
        # Create output files (summary, which is displayed and
        # details, which is not displayed).
        #
        test_time   = time.time() - self.start_time
        test_time   = round(test_time, 0)
        test_time   = str(datetime.timedelta(seconds=test_time))

        DET_FILE    = open(self.det_fnam, "w")
        SUM_FILE    = open(self.sum_fnam, "w")

        DET_FILE.write("Test case  : %s\n" % self.testNum)
        DET_FILE.write("Description: %s\n" % self.testDesc)
        DET_FILE.write("Time taken : %s\n" % str(test_time))

        boolStart = False
        for i in self._commentArray:
            if not boolStart:
                boolStart = True
                DET_FILE.write("Comments   : %s\n" % i)
            else:
                DET_FILE.write("           : %s\n" % i)

        if self.failed == 0:
            res_str = "Passed"
        else:
            res_str = "FAILED <-- !"

        #
        # Get total number of tests performed.
        #
        x = self.passed + self.failed
        y = x - self.failed
        
        totals = "(%d/%d)" %(y, x)
        SUM_FILE.write("[%s] %s %s: %s\n" % ( self.testNum.center(4), 
                                              self.testDesc.ljust(80), 
                                              totals.rjust(9),  
                                              res_str))
        
        DET_FILE.write("Passed     : %s\n" % str(self.passed))
        DET_FILE.write("Failed     : %s\n" % str(self.failed))
        DET_FILE.write("RESULT     : %s\n" % res_str)
        DET_FILE.write("\n")

        x = len(self._resultArray)
        boolFail = False
        if x > 0:
            for i in self._resultArray:
                try:
                    if i[0] == "info":
                        DET_FILE.write("           - ")
                    elif i[0]:
                        DET_FILE.write("   pass    - ")
                    else:
                        DET_FILE.write("** FAIL ** - ")
                except:
                    # Sometimes a pass means that item [0] is an object!
                    DET_FILE.write("   pass    - ")

                DET_FILE.write(i[1] + "\n")
        
        DET_FILE.close()
        SUM_FILE.close()

