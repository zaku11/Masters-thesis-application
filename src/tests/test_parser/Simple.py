from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    mainClassInfo = ClassInfo("Simple")
    mainClassInfo.members.add("x")
    for letter in ["f", "g", "h", "i", "j", "k", "l"]:
        method = MethodInfo(letter)
        method.memberReferences.add("x")
        mainClassInfo.methods[letter] = method
    
    ans["Simple"] = mainClassInfo
    return ans