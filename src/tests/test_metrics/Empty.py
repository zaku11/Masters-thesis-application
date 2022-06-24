import sys
sys.path.append("../../parser/")
from JavaParserVisitor import ClassInfo, MethodInfo

def testClass():
    mainClassInfo = ClassInfo("Simple")
    letters = ["x", "y", "z"]
    for letter in letters:
        mainClassInfo.members.add(letter)

    for methodLetter in ["f", "g", "h", "i", "j", "k"]:
        method = MethodInfo(methodLetter)
        mainClassInfo.methods[methodLetter] = method
    
    return mainClassInfo