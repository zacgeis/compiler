from utils import *
from parse import *

# TODO: we need a list of all temp variable to allocate the correct stack size

class FunctionSignature:
    def __init__(self, name, paramTypes, returnType):
        self.name = name
        self.paramTypes = paramTypes
        self.returnType = returnType

    def __repr__(self):
        return "{}({}): {}".format(self.name, ", ".join(self.paramTypes), self.returnType)

    def partialMatch(self, name, paramTypes):
        return self.name == name and self.paramTypes == paramTypes

    def __eq__(self, other):
        return (isinstance(other, FunctionSignature)
                and self.name == other.name
                and self.paramTypes == other.paramTypes
                and self.returnType == other.returnType)

    def __hash__(self):
        _hash = hash(self.name)
        _hash = _hash ^ hash(self.returnType)
        for paramType in self.paramTypes:
            _hash = _hash ^ hash(paramType)
        return _hash

class FunctionDetails:
    def __init__(self, signature, node):
        self.signature = signature
        self.node = node
        self.localVariables = {}

class ProgramDetails:
    def __init__(self, functions, globalVariables):
        self.functions = functions
        self.globalVariables = globalVariables

# At this point static analysis is pretty basic
# TODO: Eventually this should handle things like expanding templates / generics
# TODO: also handle type inference
# TODO: also handle auto casting
# TODO: variable position (of type) will be helpful when resolving types
# Think about how to support this better with generic / etc
BUILTINS = {
        FunctionSignature("+", ["int", "int"], "int"): None,
        FunctionSignature("-", ["int", "int"], "int"): None,
        FunctionSignature("*", ["int", "int"], "int"): None,
        FunctionSignature("/", ["int", "int"], "int"): None,
        FunctionSignature("==", ["int", "int"], "int"): None,
        FunctionSignature("=", ["int", "int"], "int"): None,
        FunctionSignature("!=", ["int", "int"], "int"): None,
}

class Analyzer:
    def __init__(self, nodes, originalString):
        self.nodes = nodes
        self.originalString = originalString
        self.inFunction = False
        self.currentFunction = None
        self.errors = []

        self.globalVariables = {}
        self.builtinFunctions = BUILTINS
        self.functions = {}

    def analyze(self):
        for node in self.nodes:
            self.firstPass(node)
        for node in self.nodes:
            self.secondPass(node)
        if self.hasErrors():
            self.displayAnalysisErrors()
            raise Exception("Analysis errors")
        return ProgramDetails(self.functions, self.globalVariables)

    # In-order tree traversal - we'll use this approach for emitting the instructions too
    def firstPass(self, node):
        if isinstance(node, GlobalDeclarationNode):
            if self.inFunction: raise Exception("Found a GlobalDeclarationNode while in a function.")
            self.globalVariables[node.variable.name] = node
        elif isinstance(node, FunctionNode):
            if self.inFunction: raise Exception("Found a FunctionNode while in a function.")
            functionSignature = self.functionSignatureFromFunctionNode(node)
            functionDetails = FunctionDetails(functionSignature, node)
            self.functions[functionSignature] = functionDetails
            self.inFunction = True
            self.currentFunction = functionDetails
            for statement in node.statements:
                self.firstPass(statement)
            self.inFunction = False
            self.currentFunction = None

    # In-order tree traversal - we'll use this approach for emitting the instructions too
    def secondPass(self, node):
        if isinstance(node, DeclarationNode):
            if not self.inFunction: raise Exception("Found a GlobalDeclarationNode while in global.")
            self.currentFunction.localVariables[node.variable.name] = node
        elif isinstance(node, FunctionNode):
            if self.inFunction: raise Exception("Found a FunctionNode while in a function.")
            functionSignature = self.functionSignatureFromFunctionNode(node)
            functionDetails = self.functions[functionSignature]
            self.inFunction = True
            self.currentFunction = functionDetails
            for statement in node.statements:
                self.secondPass(statement)
            self.inFunction = False
            self.currentFunction = None
        elif isinstance(node, ReturnNode):
            # TODO: we can check the type here
            if node.expression is not None:
                self.secondPass(node.expression)
        elif isinstance(node, IfNode):
            # TODO: we can check the conditional type here
            for statement in node.statements:
                self.secondPass(statement)
        elif isinstance(node, WhileNode):
            # TODO: we can check the conditional type here
            for statement in node.statements:
                self.secondPass(statement)
        elif isinstance(node, CallNode):
            # Will raise an exception if it's not found
            self.findFunctionSignatureFromCallNode(node)
        elif isinstance(node, IdentifierNode):
            # Will raise an exception if it's not found
            self.findIdentifierDeclaration(node)
        elif isinstance(node, LiteralNode):
            pass
        elif isinstance(node, VariableNode):
            pass

    def functionSignatureFromFunctionNode(self, node):
        name = node.name
        returnType = node.type
        paramTypes = []
        for variableNode in node.parameters:
            paramTypes.append(variableNode.type)
        return FunctionSignature(name, paramTypes, returnType)

    def findIdentifierDeclaration(self, node):
        if self.inFunction:
            if node.value in self.currentFunction.localVariables:
                return self.currentFunction.localVariables[node.value]
        if node.value in self.globalVariables:
            return self.globalVariables[node.value]
        self.addAnalysisError(node.pos, "Declaration not found: '{}'.".format(node.value))
        return None

    def findFunctionSignatureFromCallNode(self, callNode):
        identifier = callNode.identifier
        argTypes = []
        for argNode in callNode.arguments:
            argTypes.append(self.getType(argNode))
        # TODO: We can probably speed this up quite a bit with a hash approach
        for functionSignature in self.builtinFunctions.keys():
            if functionSignature.partialMatch(identifier, argTypes):
                return functionSignature
        for functionSignature in self.functions.keys():
            if functionSignature.partialMatch(identifier, argTypes):
                return functionSignature
        self.addAnalysisError(callNode.pos, "Function signature not found: {}({}).".format(identifier, ", ".join(argTypes)))
        return None

    def getType(self, node):
        if isinstance(node, IdentifierNode):
            return self.findIdentifierDeclaration(node).variable.type
        elif isinstance(node, CallNode):
            return self.findFunctionSignatureFromCallNode(node).returnType
        elif isinstance(node, LiteralNode):
            return node.type
        else:
            raise Exception("Invalid attempt to get type on '{}'".format(node))

    def addAnalysisError(self, pos, message):
        self.errors.append((pos, message))

    def hasErrors(self):
        return len(self.errors) > 0

    def displayAnalysisErrors(self):
        for pos, message in self.errors:
            displayError(self.originalString, pos, message)
