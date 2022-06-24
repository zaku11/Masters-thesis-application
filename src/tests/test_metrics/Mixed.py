import sys
sys.path.append("../../parser/")
from JavaParserVisitor import ClassInfo, MethodInfo

def testClass():
    mainClassInfo = ClassInfo("Simple")
    letters = ["x", "y", "z", "p"]
    for letter in letters:
        mainClassInfo.members.add(letter)

    appearances = [["x", "y"], ["x", "z"], ["x"]]
    methods = ["f", "g", "h"]

    for i in range(len(methods)):
        method = MethodInfo(methods[i])
        method.memberReferences.update(appearances[i])
        method.methodReferences.update("h")
        mainClassInfo.methods[methods[i]] = method    

    return mainClassInfo