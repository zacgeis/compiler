from utils import *

# TODO: we need a list of all temp variable to allocate the correct stack size

class FunctionSummary:
    def __init__(self, name, paramTypes, returnType):
        self.name = name
        self.paramTypes = paramTypes
        self.returnType = returnType

    def __repr__(self):
        return "{}({}): {}".format(self.name, ", ".join(self.paramTypes), self.returnType)

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

class ProgramDetails:
    def __init__(self):
        self.globalVariables = {}
        self.functions = {}

class FunctionDetails:
    def __init__(self):
        self.summary = None
        self.localVariables = {}

class Analyzer:
    def __init__(self, nodes):
        pass



