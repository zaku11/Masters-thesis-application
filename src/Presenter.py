from itertools import combinations
import os, sys
import jsonpickle
import json
from math import floor
import matplotlib.pyplot as plt
import requests
from requests.auth import HTTPBasicAuth
from scipy.stats import pearsonr, spearmanr
import numpy as np
import itertools

import time
from Credentials import getPasswd, getUsername # This will crash for you
sys.path.append("./parser/")

from JavaParserVisitor import deserializeClassInfo
from Statistics import calculateStatistics

SCORES_PREFIX = "../scores/"
GRAPHS = "../graphs/"
ALL_CALCULATED_METRICS = ["SCOM", "LSCC", "CC", "LCOM5", "CBAMU"]

metricsOrder = ['CC', 'LSCC', 'SCOM', 'CBAMU', 'LCOM5']
DEC_PLACES = 4

# Here lies the correlations
# It consists of triples : 
#       1. Name of the metadata value
#       2. Metric name - one of LSCC, LCOM - see /src/metrics/ for further reference
#       3. Function name - one of "getAverage, getMax, getMin, getVariance" - see Statistics.py for further reference

PROPERTIES = ['stargazers_count', '__java_files_loc', '__project_size', 'contributors_url', 'forks_count', 'commits_url']
FUNCS = ['getAverageWeighted']
INTERESTING_CORRELATIONS = list(itertools.product(
    PROPERTIES,
    ALL_CALCULATED_METRICS,  
    FUNCS
))

def mapPropertiesAccurate(property):
    myMap = {
        'stargazers_count': "liczby osób, które obserwują projekt",
        '__java_files_loc': "liczby linii kodu java w projekcie",
        '__project_size': "rozmiaru projektu w bajtach",
        'contributors_url': "liczby kontrybutorów",
        'forks_count': "liczby forków danego projektu",
        'commits_url': "liczby commitów w danym projekcie"
    }
    return myMap[property]

def mapProperties(property):
    myMap = {
        'stargazers_count': "Liczba osób, które obserwują projekt",
        '__java_files_loc': "Liczba linii kodu java w projekcie",
        '__project_size': "Rozmiar projektu w bajtach",
        'contributors_url': "Liczba kontrybutorów",
        'forks_count': "Liczba forków danego projektu",
        'commits_url': "Liczba commitów w danym projekcie"
    }
    return myMap[property]


if __name__ == "__main__":
    allInformation = []
    for repoNum in os.listdir(SCORES_PREFIX): # RepoNum is the repository number which we will use to identify it
        if repoNum == 'README':
            continue
        print(repoNum)
        repoPath = SCORES_PREFIX + repoNum
        with open(repoPath + "/__metadata__.json") as metadata_file:
            metadata = json.loads(metadata_file.read()) 
            if (not "metricScores.json" in os.listdir(repoPath) or
                os.path.getsize(repoPath + "/metricScores.json") == 0 or
                sorted(list(jsonpickle.decode(open(repoPath + "/metricScores.json").read()).keys())) != sorted(ALL_CALCULATED_METRICS)):
                
                classInfo = deserializeClassInfo(open(repoPath + "/classInfo.json").read())
                metricScores = dict()
                for metric in ALL_CALCULATED_METRICS:
                    metricScores[metric] = calculateStatistics(classInfo, metric)
                print(repoNum, "didn't have calculated metrics, calculated", ALL_CALCULATED_METRICS)
                allInformation.append((metadata, metricScores))

                open(repoPath + "/metricScores.json", "w+").write(jsonpickle.encode(metricScores))
            else:
                allInformation.append((metadata, jsonpickle.decode(open(repoPath + "/metricScores.json").read())))

    if '--interesting-correlations' in sys.argv:
        latexLog = ""
        for (xAxisName, yAxisName, fnToCall) in INTERESTING_CORRELATIONS:
            xAxis = []
            yAxis = []
            values = []

            for (metadata, scores) in allInformation:
                # print("{} : {}/{}".format(xAxisName, len(values), len(allInformation)))
                valueToAdd = None
                if (xAxisName.endswith("url")):
                    if(metadata.get(xAxisName + '_calculated', None) == None): 
                        pageNum = 1
                        valueToAdd = 0
                        while True:
                            urlPrefix = metadata[xAxisName]
                            if urlPrefix.endswith('{/sha}'):
                                urlPrefix = urlPrefix[:-(len('{/sha}'))]
                            req = requests.get(urlPrefix + '?per_page=100&page=' + str(pageNum), auth=HTTPBasicAuth(getUsername(), getPasswd()))
                            while req.status_code != 200:
                                if req.status_code == 404:
                                    break
                                print("Timeout while calling API. Sleeping for 5 mins", flush=True)
                                time.sleep(300)
                                req = requests.get(metadata[xAxisName], auth=HTTPBasicAuth(getUsername(), getPasswd()))

                            content = req.content.decode('utf-8')                         
                            newVal = len(json.loads(content))
                            valueToAdd += newVal
                            if newVal < 100:
                                break
                            pageNum += 1

                        metadata[xAxisName + '_calculated'] = valueToAdd
                        metadata_file = SCORES_PREFIX + str(metadata['id']) + '/__metadata__.json'
                        repoMetadata = open(metadata_file, "w")
                        repoMetadata.write(json.dumps(metadata)) 
                        print("Repo {} didn't have calculated {}, now it has".format(metadata['id'], xAxisName))
                    else:
                        # print("Nice! Repo {} already has {}".format(metadata['id'], xAxisName))
                        valueToAdd = metadata[xAxisName + '_calculated']    
                else:
                    valueToAdd = metadata[xAxisName]

                # That's a triplet: 
                # 1. Which metric e.g. LSCC + which statistic value e.g. average
                # 2. Other axis e.g. stargazers_count, java_loc
                # 3. Repository id 
                values.append((getattr(scores[yAxisName], fnToCall)(), valueToAdd, metadata['id']))


            plt.plot([val[1] for val in values], [val[0] for val in values], 'ro', markersize=2)
            plt.xlabel(mapProperties(xAxisName))
            yAxisFullName = yAxisName + "." + fnToCall 
            plt.ylabel(yAxisName)        

            titleText = ""
            latexLog += "Correlations between " + xAxisName + " and " + yAxisFullName + "\n"
            for (funcName, func) in [("Pearson", pearsonr), ("Spearman", spearmanr)]:
                funcVal = func([val[0] for val in values], [val[1] for val in values])[0]
                titleText += "{}: {}\n".format(funcName, funcVal)

            latexLog += (titleText + "\n")
            plt.title("Zestawienie wartości średnich ważonych metryki " + yAxisName + "\n i " + mapPropertiesAccurate(xAxisName), fontsize = 10)
            plt.xscale('log')

            plt.gca().set_ylim([0, 1])

            plt.savefig(GRAPHS + xAxisName + "__BY__" + yAxisFullName + "__SAMPLE__" + str(len(values)) + ".png")
            print("Generated a (", xAxisName, ",", yAxisFullName, ")")
            plt.clf()

        original_stdout = sys.stdout # Save a reference to the original standard output
        with open('LatexInterestingCorrelations.txt', 'w') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print(latexLog)
            sys.stdout = original_stdout # Reset the standard output to its original value
        print("Latex strings dumped")


    if '--metric-correlations' in sys.argv:
        fnToCall = 'getAverageWeighted'
        latexAnswers = [[[0,0] for _ in range(len(metricsOrder))] for _ in range(len(metricsOrder))]
        print("CORRELATIONS BETWEEN METRICS")
        for (metric1, metric2) in list(combinations(ALL_CALCULATED_METRICS, 2)):
            values = []
            for (metadata, metricScores) in allInformation:
                id = metadata['id']
                values.append((
                    getattr(metricScores[metric1], fnToCall)(),
                    getattr(metricScores[metric2], fnToCall)()
                ))

            titleText = ""
            for (funcName, func) in [("Pearson", pearsonr), ("Spearman", spearmanr)]:
                funcValue = func([val[0] for val in values], [val[1] for val in values])[0]
                titleText += "{}: {}\n".format(funcName, funcValue) 
                print("{} test for {}, {}, {} : {}".format(
                    funcName,
                    metric1,
                    metric2,    
                    fnToCall,
                    func([val[0] for val in values], [val[1] for val in values])
                ))
                ind = metricsOrder.index(metric1)
                ind2 = metricsOrder.index(metric2)
                if funcName == "Pearson":
                    Z = 0
                else: 
                    Z = 1
                latexAnswers[ind][ind2][Z] = funcValue
                latexAnswers[ind2][ind][Z] = funcValue

                diff = func([val[0] for val in values], [val[1] for val in values])[0] - func([val[1] for val in values], [val[0] for val in values])[0] 
                if not (-0.0001 < diff and diff < 0.0001):
                    raise Exception("The coefficient value has two distinct values!")

            plt.title("Zestawienie metryk " + metric1 + " i " + metric2)

            plt.plot([val[0] for val in values], [val[1] for val in values], 'ro', markersize=2)
            plt.xlabel(metric1)
            plt.ylabel(metric2)        
            x = np.linspace(0, 1, 10000)
            plt.plot(x, x)
            plt.plot(x, list(map(lambda y: 1 - y, x)))

            plt.savefig(GRAPHS + metric1 + "_VS_" + metric2 + ".png")
            plt.clf()

        for Z in [0, 1]:
            latexStr = ""
            latexStr += "& " + " & ".join(metricsOrder) + "\n"
            index = 0
            for wholeRow in latexAnswers:
                newRowStr = str(metricsOrder[index]) + " & "
                newRowStr += " & ".join([str(round(x[Z], DEC_PLACES)) if x[Z] != 0 else "  --  " for x in wholeRow])
                newRowStr += "\\\\ \\hline" + "\n"
                latexStr += newRowStr
                index += 1

            original_stdout = sys.stdout # Save a reference to the original standard output
            with open('LatexMetricCorrelations' + str(Z) + '.txt', 'w') as f:
                sys.stdout = f # Change the standard output to the file we created.
                print(latexStr)
                sys.stdout = original_stdout # Reset the standard output to its original value
        print("Latex strings dumped")

