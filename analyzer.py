from utils import *

class VariableDetail:
    def __init__(self, name, _type):
        self.name = name
        self.type = _type

    def __repr__(self):
        return "{}: {}".format(self.name, self._type)

    def __eq__(self, other):
        return (isinstance(other, FunctionSignature)
                and self.name == other.name
                and self.type == other.type)

class FunctionSignature:
    def __init__(self, paramTypes, returnType):
        self.paramTypes = paramTypes
        self.returnType = returnType

    def __repr__(self):
        return "({}): {}".format(", ".join(self.paramTypes), self.returnType)

    def __eq__(self, other):
        return (isinstance(other, FunctionSignature)
                and self.paramTypes == other.paramTypes
                and self.returnType == other.returnType)

class ProgramDetails:
    def __init__(self):
        self.globalVariables = {}
        self.functions = {}

class FunctionDetails:
    def __init__(self):
        self.signature = None
        self.localVariables = {}

class Analyzer:
    def __init__(self, nodes):
        pass
