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
import importlib
import os
import json

METRICSPATH = "./../../metrics/"

sys.path.append(METRICSPATH)
testedMetrics = ["SCOM", "LSCC", "CC", "LCOM5", "CBAMU"]

def reasonablyEqual(x, y):
    if (abs(x - y) < 0.0001):
        return True
    return False

def main(argv):
    correctTests = 0
    failedTests = 0

    metricFunctions = dict()
    for metric in testedMetrics:
        metricModule = importlib.import_module(metric)
        metricFunctions[metric] = metricModule.calculateCohesion

    for file in os.listdir("./"):
        if file.endswith(".py") and not file == __file__:
            answerFile = file[:-3]
            testInstance = importlib.import_module(answerFile).testClass()
            for (metricName, metricFunction) in metricFunctions.items():
                testFileName = answerFile + ".json"
                answers = json.loads(open(testFileName).read())
                if(reasonablyEqual(answers[metricName], metricFunction(testInstance))):            
                    print(bcolors.OKGREEN, bcolors.BOLD, "PASSED", end = "", sep="")
                    correctTests += 1
                else:
                    print(bcolors.FAIL, bcolors.BOLD, "FAILED", end = "", sep="")
                    print(bcolors.RESET, "expected", answers[metricName], "but got", metricFunction(testInstance), end = "")
                    failedTests += 1 
                print(bcolors.RESET, "Test", testFileName, "for metric", metricName)

    print("SUMMARY OF METRIC TESTS:", bcolors.BOLD, correctTests, "/", correctTests + failedTests,"= ", end = "")
    if(failedTests == 0):
        print(bcolors.OKGREEN, end = "")
    else: 
        print(bcolors.FAIL, end = "")

    print(correctTests * 100 / (correctTests + failedTests),"%")
    print(bcolors.RESET, end = "")

if __name__ == '__main__':
    main(sys.argv)

