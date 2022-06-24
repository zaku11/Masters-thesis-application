import sys
import importlib

sys.path.append("./parser/")
sys.path.append("./metrics/")
from JavaParserVisitor import deserializeClassInfo

class InterestingStatistics:
    classValues = [] # A list of pairs (value, weight)

    def __init__(self):
        self.classValues = []
    
    def getMetrics(self):
        sumOfSquares = 0
        sum = 0
        for (val, _) in self.classValues:
            sum += val
            sumOfSquares += val * val
        return (sum, sumOfSquares, len(self.classValues))


    def getVariance(self):
        (sum, sumOfSquares, howMany) = self.getMetrics()
        if howMany > 0:
            return (sumOfSquares - ((sum * sum) / howMany)) / howMany
        else:
            return 0
            
    def getAverage(self):
        (sum, _, howMany) = self.getMetrics()
        if howMany > 0:
            return sum / howMany
        else:
            return 0

    def getAverageWeighted(self):
        howMany = len(self.classValues)
        if(howMany == 0):
            return 0

        weightedSum = 0
        for (val, weight) in self.classValues:
            weightedSum += (val * weight)

        return weightedSum / (sum(classVal[1] for classVal in self.classValues))

    def getMax(self):
        if(len(self.classValues) == 0):
            return None
        return max(classVal[0] for classVal in self.classValues)

    def getMin(self):
        if(len(self.classValues) == 0):
            return None
        return min(classVal[0] for classVal in self.classValues)

    def addValue(self, value, weight):
        self.classValues.append((value, weight))

    def __str__(self):
        return "Minimum : {}\nMaximum : {}\nAverage : {}\nVariance : {}\n".format(
            self.getMin(), self.getMax(), self.getAverage(), self.getVariance()
        )

def calculateStatistics(classInfo, metricName):
    try:
        metric = importlib.import_module(metricName).calculateCohesion
    except:
        print("ERROR : Couldn't load metric", metricName)
        return None
    
    stats = InterestingStatistics()
    for singleInfo in classInfo.values():
        value = metric(singleInfo)
        stats.addValue(value, singleInfo.span)
    return stats


if __name__ == '__main__':
    if(len(sys.argv) == 2):
        statisticsFile = sys.argv[1]
        classData = deserializeClassInfo(open(statisticsFile, "r").read())
        if(classData != None):
            print("Data parsed succesfully")
        else:
            print("Error : couldn't parse file", statisticsFile)
 
    else:
        print("Wrong number of arguments. 1 argument expected.")


