from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    
    _subnote = "  |__ ";

    def logResult(self, p_result, p_msg, p_fnam=False):
        #
        # Add a test result to the result array.
        # Everything after the first "|" is a 'note' line for this message
        # (will be put on a separate line with _subnote prefixed).
        #
        
        # If we have filename details then add them to the message as note lines.
        if p_fnam:
            p_msg = p_msg + "|current html source = " + p_fnam[0]
            p_msg = p_msg + "|current screenshot  = " + p_fnam[1]

        #
        # The double brackets is intentional (add a 2 part
        # array: true/false/info + message).
        #
        msgArr = p_msg.split("|")        
        self._resultArray.append(("info"," "))          # (blank newline)
        self._resultArray.append((p_result, msgArr[0])) # (the main message)
        for i in range(1, len(msgArr)):                 # (any 'notes' for this message)
            self._resultArray.append(("info", self._subnote + msgArr[i]))
        
    
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
                        DET_FILE.write("             ")
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

