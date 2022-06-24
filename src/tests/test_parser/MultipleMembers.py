from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    multipleMembers = ClassInfo("MultipleMembers")
    multipleMembers.possibleFather = "FatherTwo"
    for letter in ["x", "y", "z"]:
        multipleMembers.members.add(letter)

    multipleMembers.methods["sum"] = MethodInfo("sum")

    multipleMembers.methods["sumFirst"] = MethodInfo("sumFirst")
    multipleMembers.methods["sumFirst"].memberReferences.add("x")
    multipleMembers.methods["sumFirst"].memberReferences.add("y")
    
    multipleMembers.methods["sumSecond"] = MethodInfo("sumSecond")
    multipleMembers.methods["sumSecond"].memberReferences.add("z")
    multipleMembers.methods["sumSecond"].methodReferences.add("sumFirst")

    ans["MultipleMembers"] = multipleMembers

    fatherOne = ClassInfo("FatherOne")
    fatherOne.members.add("a")
    ans["FatherOne"] = fatherOne

    fatherTwo = ClassInfo("FatherTwo")
    fatherTwo.possibleFather = "FatherOne"
    fatherTwo.members.add("b")
    ans["FatherTwo"] = fatherTwo


    return ans

