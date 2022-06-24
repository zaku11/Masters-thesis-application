from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    cl1 = ClassInfo("Test")
    cl1.members.add("foo")
    cl1.span = 6

    m1 = MethodInfo("g")
    m1.memberReferences.add("foo")
    cl1.methods["g"] = m1
    ans["Test"] = cl1


    cl2 = ClassInfo("Test2")
    cl2.span = 0
    ans["Test2"] = cl2

    cl3 = ClassInfo("Test3")
    for letter in ["x", "y", "z"]:
        cl3.members.add(letter)
    cl3.span = 1
    ans["Test3"] = cl3

    cl4 = ClassInfo("Test4")
    for letter in ["x", "y", "z"]:
        cl4.members.add(letter)
    cl4.span = 2
    ans["Test4"] = cl4

    cl5 = ClassInfo("Test5")
    for letter in ["f", "g", "h"]:
        cl5.methods[letter] = MethodInfo(letter)
    cl5.span = 10
    ans["Test5"] = cl5

    
    return ans