from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    inDir1 = ClassInfo("InDir1")
    inDir1.members.add("x")
    inDir1.methods["f"] = MethodInfo("f")

    inDir2 = ClassInfo("InDir2")
    inDir2.members.add("y")
    inDir2.methods["g"] = MethodInfo("g")
    inDir2.methods["g"].memberReferences.add("y")
    inDir2.methods["g"].methodReferences.add("g")
    
    inDir3 = ClassInfo("InDir3")
    inDir3.members.add("z")

    ans["InDir1"] = inDir1
    ans["InDir2"] = inDir2
    ans["InDir3"] = inDir3
    
    return ans

def otherStats():
    return (3,0)