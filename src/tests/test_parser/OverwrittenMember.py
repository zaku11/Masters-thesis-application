from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    mainClassInfo = ClassInfo("OverwrittenMember")
    mainClassInfo.members.add("x")
    for letter in ["f", "g"]:
        newMethod = MethodInfo(letter)
        mainClassInfo.methods[letter] = newMethod
    
    ans["OverwrittenMember"] = mainClassInfo
    return ans

