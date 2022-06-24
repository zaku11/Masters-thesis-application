import os, sys
import shutil
import jsonpickle
sys.path.append("./parser/")

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

from Parser import parseIntoClassInfo
from JavaParserVisitor import serializeClassInfo, makeVarReferencesTransitive
from Statistics import calculateStatistics
from GithubFetcher import GithubFetcher

REPOS_PREFIX = "../repos/"
ANSWERS_PREFIX = "../scores/"
ALL_CALCULATED_METRICS = ["SCOM", "LSCC", "CC", "LCOM5", "CBAMU"]

# Here we implicitly invoke makeVarReferencesTransitive!!!
def processRepo(repoNum):
    print(repoNum, ": begin processing")

    (classInfo, (parseOK, parseFails)) = (parseIntoClassInfo(REPOS_PREFIX + repoNum))
    makeVarReferencesTransitive(classInfo)
    
    print(repoNum, ": all files parsed")
    if (not os.path.exists(ANSWERS_PREFIX + repoNum)):
        os.mkdir(ANSWERS_PREFIX + repoNum)
    try:
        shutil.copy(REPOS_PREFIX + repoNum + "/__metadata__.json", ANSWERS_PREFIX + repoNum + "/__metadata__.json")
    except FileNotFoundError:
        print(bcolors.FAIL, bcolors.BOLD, "ERROR: No metadata found.", bcolors.RESET, sep="")

    open(ANSWERS_PREFIX + repoNum + "/classInfo.json", "w+").write(serializeClassInfo(classInfo))
    
    if (10 * parseFails > parseFails + parseOK):
        open(ANSWERS_PREFIX + repoNum + "/FAILED.txt", "w+").write("FAILED")

    print(repoNum, ": data dumped")
    if ("--full" in sys.argv):
        metricScores = dict()
        for metric in ALL_CALCULATED_METRICS:
            metricScores[metric] = calculateStatistics(classInfo, metric)

        open(ANSWERS_PREFIX + repoNum + "/metricScores.json", "w+").write(jsonpickle.encode(metricScores))
        print(repoNum, ": metrics calculated")
    print(repoNum, ": ended processing")

if __name__ == "__main__":
    if("--online" in sys.argv):
        HOW_MANY_REPOS = 520
        fetcher = GithubFetcher()
        for i in range(HOW_MANY_REPOS):
            thisRepoDir = fetcher.getARepoWithMetadata()
            print(thisRepoDir)
            processRepo(os.path.basename(os.path.normpath(thisRepoDir)))
            shutil.rmtree(thisRepoDir)
    else:
        for repoNum in os.listdir(REPOS_PREFIX): # RepNum is the repository number which we will use to identify it
            processRepo(repoNum)

        
        