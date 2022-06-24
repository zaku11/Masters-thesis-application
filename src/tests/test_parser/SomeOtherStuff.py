from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    mainClassInfo = ClassInfo("Stuff")
    
    mainClassInfo.methods["f"] = MethodInfo("f")
    method = MethodInfo("g")
    method.methodReferences.add("f")
    mainClassInfo.methods["g"] = method
    mainClassInfo.methods["foo"] = MethodInfo("foo")

    for meth in ["goo", "goo2", "goo3", "goo4"]:
        method2 = MethodInfo(meth)
        method2.methodReferences.add("foo")
        mainClassInfo.methods[meth] = method2

    for num in ["1", "2", "3", "4", "5"]:
        fullName = "somethingElse" + num
        method2 = MethodInfo(fullName)
        method2.methodReferences.add("foo")
        method2.methodReferences.add("f")
        mainClassInfo.methods[fullName] = method2


    ans["Stuff"] = mainClassInfo
    
    return ans