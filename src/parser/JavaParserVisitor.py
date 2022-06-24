# Generated from JavaParser.g4 by ANTLR 4.7.2
from antlr4 import *
import jsonpickle
from keyword import iskeyword
import sys

sys.setrecursionlimit(10**6)
if __name__ is not None and "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# You might ask yourself why do sort all of those things?
# That is to erase any form of dependency of the order how things were added
# Makes doing tests WAY easier when you don't have to cherrypick 
def classInfoReadable(classes, withSizes = False): #Dict of ClassInfo
    if(classes == None):
        return None
    buffer = ""
    for _, classInfoInstance in sorted(classes.items()):
        buffer += "Class {} inheriting from {}\n".format(classInfoInstance.className, classInfoInstance.possibleFather)
        if(withSizes):
            buffer += "It has a span of " + str(classInfoInstance.span)
        buffer += "Members : "
        for member in sorted(classInfoInstance.members):
            buffer += member + " "

        buffer += "\nMethods : "
        for methodName in sorted(classInfoInstance.methods.keys()):
            buffer += methodName + ","
        buffer += "\n"

        for method in sorted(classInfoInstance.methods.values()):
            buffer += "Method called " + method.methodName + " references members : "
            for var in sorted(method.memberReferences):
                buffer += var + " "
            buffer += "\nAlso that method references other methods : "
            for otherMethod in sorted(method.methodReferences):
                buffer += otherMethod + " " 
            buffer += "\n\n"
    return buffer

def serializeClassInfo(classes):
    jsonpickle.set_encoder_options('simplejson', sort_keys = True)
    return jsonpickle.encode(classes)

def deserializeClassInfo(classes):
    try:
        jsonpickle.set_decoder_options('simplejson')
        return jsonpickle.decode(classes)
    except:
        return None

def decapitalize(s):
  return ''.join([s[:1].lower(), (s[1:])])

def deleteGettersAndSetters(classes):
    for info in classes.values():
        members = info.members
        forbiddenNames = (list(map(lambda mem: "get" + decapitalize(mem) , members)) + 
                         list(map(lambda mem: "get" + mem.capitalize() , members)) +
                         list(map(lambda mem: "set" + decapitalize(mem) , members)) + 
                         list(map(lambda mem: "set" + mem.capitalize() , members)))

        for method in list(info.methods.values()):
            if(method.methodName in forbiddenNames):
                varName = method.methodName[3:]
                if((method.memberReferences == {varName.capitalize()} or 
                    method.memberReferences == {decapitalize(varName)}) and
                   len(method.methodReferences) == 0):

                    del info.methods[method.methodName]



# We need to filter out some irrelevant trash, like members of our parent class or methods
# Or even some other variables that we couldn't classify before
def filterClassesInfo(classes):
    for info in classes.values():
        methodsNames = info.methods.keys()
        members = info.members
        for method in info.methods.values():
            for var in method.memberReferences.copy():
                if (not var in members): # Some global stuff, or possibly parent member 
                    method.memberReferences.remove(var)
            for methodReference in method.methodReferences.copy():
                if (not methodReference in methodsNames):
                    method.methodReferences.remove(methodReference) 

# This, on default, is not used.
# Should this always be taken into account? I don't know, I probably will use it
# But I see reasons why You wouldn't want it
def makeVarReferencesTransitive(classes):
    def getReachableVars(classes, className, methodName):
        vis = set()
        def DFS(currMethod):
            allReachables = set()
            allReachables.update(classes[className].methods[currMethod].memberReferences)
            for method in classes[className].methods[currMethod].methodReferences:
                if(not method in vis):
                    vis.add(method)
                    allReachables.update(DFS(method))
            return allReachables
        return DFS(methodName)

    for classInfo in classes.values():
        for method in classInfo.methods.values():
            allReachableVars = getReachableVars(classes, classInfo.className, method.methodName)
            method.memberReferences.update(allReachableVars)

# What do we need to know about a method : 
#   1. Which variables/members does it reference
#   2. Which other methods does it reference  
class MethodInfo:
    methodName = ""
    memberReferences = set()
    methodReferences = set()
    def __lt__(self, other):
        return self.methodName < other.methodName

    def __init__(self, name):
        self.methodName = name
        self.memberReferences = set()
        self.methodReferences = set()

class ClassInfo:
    methods = dict() # Dict of MethodInfo
    members = set() # Set of Strings
    span = 0
    className = ""
    possibleFather = ""
    def __init__(self, name):
        self.className = name
        self.methods = dict()
        self.members = set()
        self.span = 0
        self.possibleFather = ""

# This class defines a complete generic visitor for a parse tree produced by JavaParser.

class JavaParserVisitor(ParseTreeVisitor):
    __methodSnapshot = []
    __classSnapshot = []
    __overridenNamesSnapshot = []

    insideWhichMethod = ""
    insideWhichClass = ""
    overridenNames = set() # Set of Strings
    classes = dict() # Dict of ClassInfo
    
    def __init__(self):
        self.__methodSnapshot = []
        self.__classSnapshot = []
        self.__overridenNamesSnapshot = []

        self.insideWhichMethod = ""
        self.insideWhichClass = ""
        self.overridenNames = set()
        self.classes = dict() 

    def snapshotMethod(self):
        self.__methodSnapshot.append(self.insideWhichMethod)
    def restoreMethod(self):
        assert(len(self.__methodSnapshot) > 0)
        self.insideWhichMethod = self.__methodSnapshot.pop()

    def snapshotClass(self):
        self.__classSnapshot.append(self.insideWhichClass)
    def restoreClass(self):
        assert(len(self.__classSnapshot) > 0)
        self.insideWhichClass = self.__classSnapshot.pop()

    def snapshotOverridenNames(self):
        self.__overridenNamesSnapshot.append(self.overridenNames.copy())
    def restoreOverridenNames(self):
        assert(len(self.__overridenNamesSnapshot) > 0)
        self.overridenNames = self.__overridenNamesSnapshot.pop()



    # Visit a parse tree produced by JavaParser#compilationUnit.
    def visitCompilationUnit(self, ctx:JavaParser.CompilationUnitContext):
        children = self.visitChildren(ctx) 
        deleteGettersAndSetters(self.classes)
        filterClassesInfo(self.classes)
        # makeVarReferencesTransitive(self.classes)
        return self.classes
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageDeclaration.
    def visitPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#importDeclaration.
    def visitImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:JavaParser.TypeDeclarationContext):
        # As much as I would love to do some logic, we can e.g. have a nested class parsed
        # as a member and NOT A TYPE. Which means it wouldn't be catched here.        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#modifier.
    def visitModifier(self, ctx:JavaParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classOrInterfaceModifier.
    def visitClassOrInterfaceModifier(self, ctx:JavaParser.ClassOrInterfaceModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableModifier.
    def visitVariableModifier(self, ctx:JavaParser.VariableModifierContext):
        return self.visitChildren(ctx)

    def traverse(self, ctx):
        childLen = len(ctx.children)
        for i in range(childLen):
            child = ctx.children[(childLen - 1) - i]
            if(isinstance(child, ParserRuleContext)):
                return self.traverse(child)
        return ctx.start.line

    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        className = ctx.IDENTIFIER().getText()

        self.snapshotClass()
        self.snapshotMethod()
        self.insideWhichClass = className
        self.insideWhichMethod = ""
        self.classes[className] = ClassInfo(className)
        self.classes[className].span = self.traverse(ctx) - ctx.start.line

        if(ctx.typeType() != None):
            self.classes[className].possibleFather = ctx.typeType().getText()
        
        children = self.visitChildren(ctx)
        self.restoreClass()
        self.restoreMethod()
        return children


    # Visit a parse tree produced by JavaParser#typeParameters.
    def visitTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameter.
    def visitTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeBound.
    def visitTypeBound(self, ctx:JavaParser.TypeBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        return self.visitChildren(ctx)



    # Visit a parse tree produced by JavaParser#enumConstants.
    def visitEnumConstants(self, ctx:JavaParser.EnumConstantsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumConstant.
    def visitEnumConstant(self, ctx:JavaParser.EnumConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumBodyDeclarations.
    def visitEnumBodyDeclarations(self, ctx:JavaParser.EnumBodyDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceDeclaration.
    def visitInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        # Currently, I don't really count interfaces as those don't really work in my context
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBody.
    def visitClassBody(self, ctx:JavaParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceBody.
    def visitInterfaceBody(self, ctx:JavaParser.InterfaceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBodyDeclaration.
    def visitClassBodyDeclaration(self, ctx:JavaParser.ClassBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#memberDeclaration.
    def visitMemberDeclaration(self, ctx:JavaParser.MemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced sby JavaParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        methodName = ctx.IDENTIFIER().getText()
        
        self.snapshotMethod()
        self.snapshotOverridenNames()

        self.insideWhichMethod = methodName
        if(self.insideWhichClass != ""): # This might be empty if this is an enum
            self.classes[self.insideWhichClass].methods[methodName] = MethodInfo(methodName)
        children = self.visitChildren(ctx)

        self.restoreOverridenNames()
        self.restoreMethod()
        return children


    # Visit a parse tree produced by JavaParser#methodBody.
    def visitMethodBody(self, ctx:JavaParser.MethodBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeTypeOrVoid.
    def visitTypeTypeOrVoid(self, ctx:JavaParser.TypeTypeOrVoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#genericMethodDeclaration.
    def visitGenericMethodDeclaration(self, ctx:JavaParser.GenericMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#genericConstructorDeclaration.
    def visitGenericConstructorDeclaration(self, ctx:JavaParser.GenericConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        # This is ALSO a copy-paste from method declaration since we don't differentiate between those two
        methodName = ctx.IDENTIFIER().getText()

        self.snapshotMethod()
        self.snapshotOverridenNames()

        self.insideWhichMethod = methodName
        if(self.insideWhichClass != ""): # This might be empty if this is an enum
            self.classes[self.insideWhichClass].methods[methodName] = MethodInfo(methodName)
        children = self.visitChildren(ctx)

        self.restoreOverridenNames()
        self.restoreMethod()
        return children


    # Visit a parse tree produced by JavaParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def visitInterfaceBodyDeclaration(self, ctx:JavaParser.InterfaceBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def visitInterfaceMemberDeclaration(self, ctx:JavaParser.InterfaceMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constDeclaration.
    def visitConstDeclaration(self, ctx:JavaParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constantDeclarator.
    def visitConstantDeclarator(self, ctx:JavaParser.ConstantDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        methodName = ctx.IDENTIFIER().getText()
        
        self.snapshotMethod()
        self.snapshotOverridenNames()

        self.insideWhichMethod = methodName
        if(self.insideWhichClass != ""): # This might be empty if this is an enum
            self.classes[self.insideWhichClass].methods[methodName] = MethodInfo(methodName)

        self.restoreOverridenNames()
        self.restoreMethod()
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodModifier.
    def visitInterfaceMethodModifier(self, ctx:JavaParser.InterfaceMethodModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#genericInterfaceMethodDeclaration.
    def visitGenericInterfaceMethodDeclaration(self, ctx:JavaParser.GenericInterfaceMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclarators.
    def visitVariableDeclarators(self, ctx:JavaParser.VariableDeclaratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclarator.
    def visitVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        varName = ctx.variableDeclaratorId().getText()  
        if(self.insideWhichClass != ""):
            if(self.insideWhichMethod == ""):
                self.classes[self.insideWhichClass].members.add(varName)
                return self.visitChildren(ctx)
            else:
                # This is made in case of things like 
                # int x := x + 1
                # Which references member x
                # And although things like this don't compile there might be another clever way to circumvent this
                children = self.visitChildren(ctx)
                self.overridenNames.add(varName)  
                return children


    # Visit a parse tree produced by JavaParser#variableDeclaratorId.
    def visitVariableDeclaratorId(self, ctx:JavaParser.VariableDeclaratorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableInitializer.
    def visitVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayInitializer.
    def visitArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classOrInterfaceType.
    def visitClassOrInterfaceType(self, ctx:JavaParser.ClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgument.
    def visitTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#qualifiedNameList.
    def visitQualifiedNameList(self, ctx:JavaParser.QualifiedNameListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameters.
    def visitFormalParameters(self, ctx:JavaParser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameterList.
    def visitFormalParameterList(self, ctx:JavaParser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameter.
    def visitFormalParameter(self, ctx:JavaParser.FormalParameterContext):
        self.overridenNames.add(ctx.variableDeclaratorId().getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lastFormalParameter.
    def visitLastFormalParameter(self, ctx:JavaParser.LastFormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#qualifiedName.
    def visitQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#literal.
    def visitLiteral(self, ctx:JavaParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#integerLiteral.
    def visitIntegerLiteral(self, ctx:JavaParser.IntegerLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#floatLiteral.
    def visitFloatLiteral(self, ctx:JavaParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#altAnnotationQualifiedName.
    def visitAltAnnotationQualifiedName(self, ctx:JavaParser.AltAnnotationQualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotation.
    def visitAnnotation(self, ctx:JavaParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValuePairs.
    def visitElementValuePairs(self, ctx:JavaParser.ElementValuePairsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValuePair.
    def visitElementValuePair(self, ctx:JavaParser.ElementValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValue.
    def visitElementValue(self, ctx:JavaParser.ElementValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(self, ctx:JavaParser.ElementValueArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeDeclaration.
    def visitAnnotationTypeDeclaration(self, ctx:JavaParser.AnnotationTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeBody.
    def visitAnnotationTypeBody(self, ctx:JavaParser.AnnotationTypeBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeElementDeclaration.
    def visitAnnotationTypeElementDeclaration(self, ctx:JavaParser.AnnotationTypeElementDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeElementRest.
    def visitAnnotationTypeElementRest(self, ctx:JavaParser.AnnotationTypeElementRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationMethodOrConstantRest.
    def visitAnnotationMethodOrConstantRest(self, ctx:JavaParser.AnnotationMethodOrConstantRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationMethodRest.
    def visitAnnotationMethodRest(self, ctx:JavaParser.AnnotationMethodRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationConstantRest.
    def visitAnnotationConstantRest(self, ctx:JavaParser.AnnotationConstantRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#defaultValue.
    def visitDefaultValue(self, ctx:JavaParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#block.
    def visitBlock(self, ctx:JavaParser.BlockContext):
        self.snapshotOverridenNames()
        children = self.visitChildren(ctx)
        self.restoreOverridenNames()
        return children


    # Visit a parse tree produced by JavaParser#blockStatement.
    def visitBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localTypeDeclaration.
    def visitLocalTypeDeclaration(self, ctx:JavaParser.LocalTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statement.
    def visitStatement(self, ctx:JavaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchClause.
    def visitCatchClause(self, ctx:JavaParser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchType.
    def visitCatchType(self, ctx:JavaParser.CatchTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#finallyBlock.
    def visitFinallyBlock(self, ctx:JavaParser.FinallyBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resourceSpecification.
    def visitResourceSpecification(self, ctx:JavaParser.ResourceSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resources.
    def visitResources(self, ctx:JavaParser.ResourcesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resource.
    def visitResource(self, ctx:JavaParser.ResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(self, ctx:JavaParser.SwitchBlockStatementGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchLabel.
    def visitSwitchLabel(self, ctx:JavaParser.SwitchLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forControl.
    def visitForControl(self, ctx:JavaParser.ForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forInit.
    def visitForInit(self, ctx:JavaParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enhancedForControl.
    def visitEnhancedForControl(self, ctx:JavaParser.EnhancedForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#parExpression.
    def visitParExpression(self, ctx:JavaParser.ParExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionList.
    def visitExpressionList(self, ctx:JavaParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodCall.
    def visitMethodCall(self, ctx:JavaParser.MethodCallContext):
        if(ctx.SUPER() == None and ctx.THIS() == None): # This is in case of super() or this() constructor
            methodName = ctx.IDENTIFIER().getText()
            if(self.insideWhichClass != "" and self.insideWhichMethod != ""):
                self.classes[self.insideWhichClass].methods[self.insideWhichMethod].methodReferences.add(methodName)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expression.
    def visitExpression(self, ctx:JavaParser.ExpressionContext):
        textList = ctx.getText().split('.')
        if(len(textList) == 2 and textList[0].isidentifier() and not iskeyword(textList[0])
            and (ctx.IDENTIFIER() != None or ctx.methodCall() != None) # This is to prevent some postfix shenanigans like this.x++
            and self.insideWhichMethod != "" and self.insideWhichClass != ""): # And to prevent things like class x{int y = this.foo()} 
            cl = textList[0]
            fieldOrMethod = textList[1]
            if(cl == "this"):
                if(fieldOrMethod.endswith(")")): # This is a method
                    pointer = len(fieldOrMethod) - 2
                    balance = 1
                    while(balance > 0 and pointer > 0):
                        if(fieldOrMethod[pointer] == "("):
                            balance -= 1
                        if(fieldOrMethod[pointer] == ")"):
                            balance += 1
                        pointer -= 1

                    pointer += 1
                    self.classes[self.insideWhichClass].methods[self.insideWhichMethod].methodReferences.add(fieldOrMethod[0:pointer])
                    if(ctx.methodCall() != None):
                        return self.visitChildren(ctx.methodCall())
                else:
                    self.classes[self.insideWhichClass].methods[self.insideWhichMethod].memberReferences.add(fieldOrMethod)
            else:
                if(ctx.IDENTIFIER() != None):
                    self.classes[self.insideWhichClass].methods[self.insideWhichMethod].memberReferences.add(cl)
            # else:
            #     return self.visitChildren(ctx)
        # IMPORTANT : HERE WE DON'T RECURSE ON OUR CHILDREN
        else: # We need to prevent things like foo.bar() when we can't establish the type of foo
            return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaExpression.
    def visitLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParameters.
    def visitLambdaParameters(self, ctx:JavaParser.LambdaParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaBody.
    def visitLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        self.snapshotOverridenNames()
        children = self.visitChildren(ctx)
        self.restoreOverridenNames()
        return children


    # Visit a parse tree produced by JavaParser#primary.
    def visitPrimary(self, ctx:JavaParser.PrimaryContext):
        # This may be empty if we do some stuff outside a method, e.g. instantiate a static attribute
        if(self.insideWhichClass != "" and self.insideWhichMethod != ""):
            firstElem = ctx.getText()
            if(not (firstElem in self.overridenNames)):
                self.classes[self.insideWhichClass].methods[self.insideWhichMethod].memberReferences.add(firstElem)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classType.
    def visitClassType(self, ctx:JavaParser.ClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#creator.
    def visitCreator(self, ctx:JavaParser.CreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#createdName.
    def visitCreatedName(self, ctx:JavaParser.CreatedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#innerCreator.
    def visitInnerCreator(self, ctx:JavaParser.InnerCreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayCreatorRest.
    def visitArrayCreatorRest(self, ctx:JavaParser.ArrayCreatorRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classCreatorRest.
    def visitClassCreatorRest(self, ctx:JavaParser.ClassCreatorRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#explicitGenericInvocation.
    def visitExplicitGenericInvocation(self, ctx:JavaParser.ExplicitGenericInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def visitTypeArgumentsOrDiamond(self, ctx:JavaParser.TypeArgumentsOrDiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#nonWildcardTypeArgumentsOrDiamond.
    def visitNonWildcardTypeArgumentsOrDiamond(self, ctx:JavaParser.NonWildcardTypeArgumentsOrDiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#nonWildcardTypeArguments.
    def visitNonWildcardTypeArguments(self, ctx:JavaParser.NonWildcardTypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeList.
    def visitTypeList(self, ctx:JavaParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeType.
    def visitTypeType(self, ctx:JavaParser.TypeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primitiveType.
    def visitPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArguments.
    def visitTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#superSuffix.
    def visitSuperSuffix(self, ctx:JavaParser.SuperSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#explicitGenericInvocationSuffix.
    def visitExplicitGenericInvocationSuffix(self, ctx:JavaParser.ExplicitGenericInvocationSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arguments.
    def visitArguments(self, ctx:JavaParser.ArgumentsContext):
        return self.visitChildren(ctx)



del JavaParser