from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    A = ClassInfo("A")
    A.members.add("z")
    A.members.add("y")
    A.methods["foo"] = MethodInfo("foo")

    B = ClassInfo("B")
    B.members.add("x")
    B.methods["bar"] = MethodInfo("bar")
    
    ans["A"] = A
    ans["B"] = B
    
    return ans