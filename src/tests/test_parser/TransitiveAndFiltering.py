from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    transitiveAndFiltering = ClassInfo("TransitiveAndFiltering")
    transitiveAndFiltering.possibleFather = "Father"
    for letter in ["x", "y", "z"]:
        transitiveAndFiltering.members.add(letter)

    transitiveAndFiltering.methods["sum"] = MethodInfo("sum")
    transitiveAndFiltering.methods["sum"].memberReferences.add("x")

    transitiveAndFiltering.methods["invoker"] = MethodInfo("invoker")
    transitiveAndFiltering.methods["invoker"].memberReferences.add("x")
    transitiveAndFiltering.methods["invoker"].methodReferences.add("sum")

    transitiveAndFiltering.methods["rec"] = MethodInfo("rec")
    transitiveAndFiltering.methods["rec"].memberReferences.add("x")
    transitiveAndFiltering.methods["rec"].methodReferences.add("rec")


    ans["TransitiveAndFiltering"] = transitiveAndFiltering

    father = ClassInfo("Father")
    father.members.add("a")
    father.methods["foo"] = MethodInfo("foo")

    ans["Father"] = father

    return ans

