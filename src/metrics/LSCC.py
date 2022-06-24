def calculateCohesion(classInfo):
    
    methodCount = len(classInfo.methods)
    varCount = len(classInfo.members)
    if(varCount == 0 and methodCount > 1):
        return 0
    
    if(varCount > 0 and methodCount == 0):
        return 1

    if(methodCount == 1):
        return 1

    if(varCount == 0 and methodCount == 0):
        return 1

    answer = 0
    for var in classInfo.members:
        howManyMethodsReferenceThis = 0
        if classInfo.methods.values() != None:
            for method in classInfo.methods.values():
                if var in method.memberReferences:
                    howManyMethodsReferenceThis += 1
            answer += howManyMethodsReferenceThis * (howManyMethodsReferenceThis - 1)
    
    answer = answer / (varCount * methodCount * (methodCount - 1))

    assert(answer <= 1)
    assert(answer >= 0)
    return answer