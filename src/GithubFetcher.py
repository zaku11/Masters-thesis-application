import requests
import json
import random
import git
import time
import os
import random
import csv


# https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
# Answer by Monkut
# Updated so I also get sum of sizes of all java files and sum of Lines Of Code in java files
def getFileSize(start_path):
    totalSize = 0
    javaFilesSize = 0
    javaFilesLOC = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                fileSize = os.path.getsize(fp)
                totalSize += fileSize
                if (os.path.splitext(fp)[-1].lower() == ".java"):
                    javaFilesSize += fileSize
                    javaFilesLOC += sum(1 for line in open(fp, encoding="ISO-8859-1"))
    return (totalSize, javaFilesSize, javaFilesLOC)



# Example request to github
# https://api.github.com/search/repositories?q=stars:%3E=1000+language:java&sort=stars&order=asc
REPO_DIR = "../repos"

# KNOWN GITHUB LIMITATIONS:
# {
#   "message": "Only the first 1000 search results are available",
#   "documentation_url": "https://docs.github.com/v3/search/"
# }


class GithubFetcher:
    def __init__(self):
        self.alreadyFetchedRepos = set()
        self.starDistribution = []
        sumOfStarCounts = 0
        with open('./GithubStarDistribution.csv', newline='') as githubStarDistribution:
            reader = csv.reader(githubStarDistribution, delimiter=';')
            for row in reader:
                starLowerBound = int(row[1])
                starUpperBound = int(row[2])
                starCount = int(row[3])
                sumOfStarCounts += starCount

                self.starDistribution.append((starLowerBound, starUpperBound, starCount))

        self.totalRepoCount = sumOfStarCounts
    
    def getRandomRepoCoords(self):
        repoNum = random.randrange(1, self.totalRepoCount + 1)
        
        print("Got a number", repoNum)
        id = 0
        while(id < len(self.starDistribution) and repoNum - self.starDistribution[id][2] > 0):
            repoNum -= self.starDistribution[id][2]
            id += 1

        starLowerBound = self.starDistribution[id][0]
        starUpperBound = self.starDistribution[id][1]
        remainder = repoNum
        print("That puts it at (", starLowerBound,"-", starUpperBound,") with num ",remainder)

        return (starLowerBound, starUpperBound, remainder)

    # Returns a string representing a query to Github API.
    def getQuery(self, starsMin, starsMax, repoNum):
        basicQuery = 'https://api.github.com/search/repositories?q=stars:{stars_min}..{stars_max}+language:java&sort=stars&order=asc&per_page=1&page={page}'
        return basicQuery.format(stars_min = starsMin, stars_max = starsMax, page = repoNum) 

    # Sends a query to Github, possibly retrying it later because of github API limits 
    def queryGithub(self, starsMin, starsMax, repoNum):
        queryResponse = json.loads(requests.get(self.getQuery(starsMin, starsMax, repoNum)).content)

        if("message" in queryResponse.keys() and queryResponse["message"].startswith("API rate limit exceeded")):
            print("Query limit exceeded. Sleeping for 30 seconds..")
            time.sleep(30)
            return self.queryGithub(starsMin, starsMax, repoNum)

        return queryResponse

    # Fetches a "random" Java repository from Github
    def getRandomRepo(self):
        
        (LBound, UBound, remainder) = self.getRandomRepoCoords()

        randomRepoQueryResponse = self.queryGithub(LBound, UBound, remainder)
        if(randomRepoQueryResponse["total_count"] == 0):
            return None

        if len(randomRepoQueryResponse["items"]) == 1:
            chosenRepo = randomRepoQueryResponse["items"][0]
            if(chosenRepo["id"] in self.alreadyFetchedRepos):
                return self.getRandomRepo()
            else: 
                self.alreadyFetchedRepos.add(chosenRepo["id"])
                return chosenRepo
        else:
            return self.getRandomRepo()

# Important note here : We will be adding some special metadata to information about repo
# At this point the highest star count is a repository with a ~117k stars
    def getARepoWithMetadata(self):

        randomRepo = self.getRandomRepo()
        if randomRepo == None:
            return self.getARepoWithMetadata()

        tmpDir = REPO_DIR + str(randomRepo["id"])
        if(os.path.isdir(tmpDir)):
            return self.getARepoWithMetadata()

        print(tmpDir)
        print("Attempting to fetch a repo from url {:1} into directory {:2}".format(randomRepo["clone_url"], tmpDir))
        git.Repo.clone_from(randomRepo["clone_url"], tmpDir) #, progress=MyProgressPrinter())

        (repoSize, javaFilesSize, javaFilesLOC) = getFileSize(tmpDir)
        randomRepo["__project_size"] = repoSize
        randomRepo["__java_files_sizes"] = javaFilesSize
        randomRepo["__java_files_loc"] = javaFilesLOC
        
        repoMetadata = open(tmpDir + "/__metadata__.json", "w")
        repoMetadata.write(json.dumps(randomRepo)) 
        
        return tmpDir

if __name__ == "__main__":
    fetcher = GithubFetcher()
    print(fetcher.getARepoWithMetadata())