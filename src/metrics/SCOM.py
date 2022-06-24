def calculateCohesion(classInfo):

    methodCount = len(classInfo.methods)
    attrCount = len(classInfo.members)

    sum = 0
    for (method1name, method1) in classInfo.methods.items():
        for (method2name, method2) in classInfo.methods.items():
            if (method1name < method2name):
                attrs1 = method1.memberReferences
                attrs2 = method2.memberReferences
                intersection = len(attrs1.intersection(attrs2))
                union = len(attrs1) + len(attrs2) - intersection
                if (intersection == 0):
                    sum += 0
                else:
                    C = intersection / min(len(attrs1), len(attrs2))
                    alpha = union / attrCount
                    sum += alpha * C
    if methodCount <= 1:
        answer = 1
    else:
        answer = sum / (methodCount * (methodCount - 1) / 2)
    assert(answer <= 1)
    assert(answer >= 0)
    return answer