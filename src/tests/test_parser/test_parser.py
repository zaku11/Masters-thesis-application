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

sys.path.append("../../parser")
from JavaParserVisitor import makeVarReferencesTransitive, classInfoReadable
from Parser import parseIntoClassInfo

IGNORED_DIRS = ["__pycache__"]

def main(argv):
    correctTests = 0
    failedTests = 0
    for file in os.listdir("./"):
        if file.endswith(".java") or (os.path.isdir(file) and file not in IGNORED_DIRS):
            answerFile = file
            if(os.path.isfile(file)): 
                answerFile = file[:-5]

            answerModule = importlib.import_module(answerFile)
            answer = parseIntoClassInfo(file)

            if(file.startswith("Transitive")): # This is hacky, but will suffice for now
                makeVarReferencesTransitive(answer)

            withSpan = False
            if(file.startswith("Span")):
                withSpan = True

            if(isinstance(answer, tuple)):
                assert(answer[1] == answerModule.otherStats())
                answer = answer[0]

            if(classInfoReadable(answer, withSpan) == classInfoReadable(answerModule.expectedAnswer(), withSpan)):            
                print(bcolors.OKGREEN, bcolors.BOLD, "PASSED", end = "", sep="")
                correctTests += 1
            else:
                import ipdb; ipdb.set_trace()
                print(bcolors.FAIL, bcolors.BOLD, "FAILED", end = "", sep="")
                failedTests += 1 
            print(bcolors.RESET, "Test", answerFile)

    print("SUMMARY OF PARSER TESTS:", bcolors.BOLD, correctTests, "/", correctTests + failedTests,"= ", end = "")
    if(failedTests == 0):
        print(bcolors.OKGREEN, end = "")
    else: 
        print(bcolors.FAIL, end = "")

    print(correctTests * 100 / (correctTests + failedTests),"%")
    print(bcolors.RESET, end = "")

if __name__ == '__main__':
    main(sys.argv)

