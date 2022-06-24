from JavaParserVisitor import ClassInfo, MethodInfo

def expectedAnswer():
    ans = dict()
    outerClass = ClassInfo("OuterClass")
    outerClass.members.add("x")

    foo = MethodInfo("foo")
    foo.memberReferences.add("x")
    outerClass.methods["foo"] = foo

    bar = MethodInfo("bar")
    outerClass.methods["bar"] = bar

    ans["OuterClass"] = outerClass

    nestedClass = ClassInfo("NestedClass")
    nestedClass.members.add("y")

    foobar = MethodInfo("foobar")
    foobar.memberReferences.add("y")
    nestedClass.methods["foobar"] = foobar

    barfoo = MethodInfo("barfoo")
    nestedClass.methods["barfoo"] = barfoo

    ans["NestedClass"] = nestedClass
    
    return ans