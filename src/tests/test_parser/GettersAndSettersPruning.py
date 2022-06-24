from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    test = ClassInfo("Test")
    test.members.add("x")
    test.members.add("y")

    test.methods["foo"] = MethodInfo("foo")

    getZ = MethodInfo("getZ")
    getZ.memberReferences.add("y")
    test.methods["getZ"] = getZ

    ans["Test"] = test
    
    return ans