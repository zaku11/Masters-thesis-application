class bcolors:
    RESET = '\u001b[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


import sys

sys.path.append("../../")
sys.path.append("../../parser")

from Statistics import InterestingStatistics


def reasonablyEqual(x, y):
    if (abs(x - y) < 0.0001):
        return True
    return False

def reasonablyEqualTuples(t1, t2):
    assert(len(t1) == len(t2))
    for i in range(len(t1)):
        if(not reasonablyEqual(t1[i], t2[i])):
            return False
    return True

def interestingValues(stats):
    return (stats.getMin(), stats.getMax(), stats.getAverage(), stats.getVariance())

class RunningModule:
    correctTests = 0
    failedTests = 0

    def runTest(self, EXPECTED_ANSWERS, ADDED_VALUES, isWeighted):
        assert(len(ADDED_VALUES) == len(EXPECTED_ANSWERS))
        for i in range(len(EXPECTED_ANSWERS)):
            valuesToAdd = ADDED_VALUES[i]
            correctAnswer = EXPECTED_ANSWERS[i]
            stats =  InterestingStatistics()
            ourAnswer = None
            if(isWeighted):
                for (val, weight) in valuesToAdd:
                    stats.addValue(val, weight)
                ourAnswer = tuple([stats.getAverageWeighted()])
            else:
                for val in valuesToAdd:
                    stats.addValue(val, 1)
                ourAnswer = interestingValues(stats)
            if(reasonablyEqualTuples(ourAnswer, correctAnswer)):
                self.correctTests += 1
            else:
                self.failedTests += 1
                print("Got ", ourAnswer, "but expected", correctAnswer)

def main(argv):
    module = RunningModule()

    # Here tests will be inlined since this is a relatively simple module
    EXPECTED_ANSWERS = [(0, 1, 0.5, 0.25), 
                        (0.25, 0.25, 0.25, 0), 
                        (0, 1, 0.4166, 0.1805), 
                        (0, 1, 0.6875, 0.1679), 
                        (0.2121, 0.412, 0.2872, 0.0060)]
    ADDED_VALUES = [[0, 1], 
                    [0.25], 
                    [1, 0, 0.25], 
                    [1, 0.75, 1, 0], 
                    [0.412, 0.234, 0.2121, 0.291]]

    module.runTest(EXPECTED_ANSWERS, ADDED_VALUES, False)

    EXPECTED_ANSWERS_WEIGHTED = list(map(lambda el: tuple([el]), [1.3333, 2.3333, 4.6585])) 
    ADDED_VALUES_WEIGHTED = [[(0, 42), (1, 42), (3, 42)], 
                             [(1, 1), (2, 2), (3, 3)],
                             [(1, 7), (3, 15), (5, 8), (9, 11)]]
    module.runTest(EXPECTED_ANSWERS_WEIGHTED, ADDED_VALUES_WEIGHTED, True)

    print("SUMMARY OF STATISTIC TESTS:", bcolors.BOLD, module.correctTests, "/", module.correctTests + module.failedTests,"= ", end = "")
    if(module.failedTests == 0):
        print(bcolors.OKGREEN, end = "")
    else: 
        print(bcolors.FAIL, end = "")

    print(module.correctTests * 100 / (module.correctTests + module.failedTests),"%")
    print(bcolors.RESET, end = "")

if __name__ == '__main__':
    main(sys.argv)

