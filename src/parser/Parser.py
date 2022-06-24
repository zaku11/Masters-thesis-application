import sys
import os
from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from JavaParserVisitor import JavaParserVisitor, classInfoReadable, serializeClassInfo
import glob


def parseIntoClassInfoSingleFile(file):
    print("File:", file)
    text = FileStream(file, encoding = "utf-8", errors = "replace")
    lexer = JavaLexer(text)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.compilationUnit()
    # print(Trees.toStringTree(tree, None, parser))        
    if parser.getNumberOfSyntaxErrors() == 0:
        answer = JavaParserVisitor().visitCompilationUnit(tree)
        return answer
    else:
        print("Code generation failed due to parsing error - returning None")
        return None

def parseIntoClassInfoMultipleFiles(dir):
    globalAnswer = dict()
    parsedFine = 0
    parsedCrash = 0
    if(not dir.endswith("/")):
        dir = dir + "/"

    for filename in glob.iglob(dir + '**/*.java', recursive=True):
        if (os.path.isfile(filename)): # C'mon, what is a directory name like org.eclipse.umlgen.reverse.java 
            localAnswer = parseIntoClassInfoSingleFile(filename)
            if(localAnswer != None):
                globalAnswer.update(localAnswer) 
                parsedFine += 1
            else:
                parsedCrash += 1
    return (globalAnswer, (parsedFine, parsedCrash))

def parseIntoClassInfo(file):
    if (os.path.isfile(file)):
        return parseIntoClassInfoSingleFile(file)
    else:
        return parseIntoClassInfoMultipleFiles(file)


if __name__ == '__main__':
    if(len(sys.argv) == 2):
        fileOrDir = sys.argv[1]
        parsedData = parseIntoClassInfo(fileOrDir)
        if(parsedData != dict()): 
            print("Parse succesfull!")
            print(classInfoReadable(parsedData, True))
            print(serializeClassInfo(parsedData))

    else:
        print("Wrong number of arguments. 1 argument expected.")


