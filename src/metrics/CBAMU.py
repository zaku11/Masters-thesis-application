def getReachableMethods(classInfo, methodName):
    vis = set()
    def DFS(currMethod):
        allReachables = set()
        allReachables.update(classInfo.methods[currMethod].methodReferences)
        for method in classInfo.methods[currMethod].methodReferences:
            if(not method in vis):
                vis.add(method)
                allReachables.update(DFS(method))
        return allReachables
    return DFS(methodName)

def calculateCohesion(classInfo):

    methodCount = len(classInfo.methods)
    atttrCount = len(classInfo.members)

    if methodCount == 0 or atttrCount == 0:
        AU = 0
    else:
        AU = 0
        for var in classInfo.members:
            if classInfo.methods.values() != None:
                for method in classInfo.methods.values():
                    if var in method.memberReferences:
                        AU += 1
        AU = AU / (methodCount * atttrCount)

    if methodCount < 2:
        CU = 0
    else:
        CU = 0
        for (method1name, _) in classInfo.methods.items():
            reachables = getReachableMethods(classInfo, method1name)
            CU += len(reachables)
            if method1name in reachables:
                CU -= 1 
        CU = CU / (methodCount * (methodCount - 1))

    answer = (AU + CU) / 2

    assert(answer <= 1)
    assert(answer >= 0)
    return answer