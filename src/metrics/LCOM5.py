def calculateCohesion(classInfo):
    
    methodCount = len(classInfo.methods)
    varCount = len(classInfo.members)
    methodVarReferenceCount = 0
    for method in classInfo.methods.values():
        methodVarReferenceCount += len(method.memberReferences)
    
    if(methodCount * varCount != 0):
        answer = 1 - (methodVarReferenceCount / (methodCount * varCount))
    else:
        answer = 0

    assert(answer <= 1)
    assert(answer >= 0)
    return answer