from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    mainClassInfo = ClassInfo("Test")
    mainClassInfo.members.add("foo")
    mainClassInfo.methods["fake"] = MethodInfo("fake")
    
    for meth in ["g", "g2", "g3", "g4", "g5"]:
        method = MethodInfo(meth)
        method.memberReferences.add("foo")
        mainClassInfo.methods[meth] = method
    
    ans["Test"] = mainClassInfo
    
    return ans