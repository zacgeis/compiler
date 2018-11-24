from utils import *

# We store references to tokens for positioning information
class NumberLiteralNode:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "NumberLiteralNode(number = '{}')".format(self.number)

    def __eq__(self, other):
        return (isinstance(other, NumberLiteralNode)
                and self.number == other.number)

class PrefixNode:
    def __init__(self, prefix, right):
        self.prefix = prefix
        self.right = right

    def __repr__(self):
        return "PrefixNode(prefix = '{}', right = '{}')".format(self.prefix, self.right)

    def __eq__(self, other):
        return (isinstance(other, PrefixNode)
                and self.prefix == other.prefix
                and self.right == other.right)

class InfixNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return "InfixNode(left = '{}', op = '{}', right = '{}')".format(self.left, self.op, self.right)

    def __eq__(self, other):
        return (isinstance(other, InfixNode)
                and self.left == other.left
                and self.op == other.op
                and self.right == other.right)

class CallNode:
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        return "CallNode(identifier = '{}', arguments = '{}')".format(self.identifier, self.arguments)

    def __eq__(self, other):
        return (isinstance(other, CallNode)
                and self.identifier == other.identifier
                and self.arguments == other.arguments)

class IfNode:
    def __init__(self, conditional, statements, elseStatements):
        self.conditional = conditional
        self.statements = statements
        self.elseStatements = elseStatements

    def __repr__(self):
        return "IfNode(conditional = '{}', statements = '{}', elseStatements = '{}')".format(self.conditional, self.statements, self.elseStatements)

    def __eq__(self, other):
        return (isinstance(other, IfNode)
                and self.conditional == other.conditional
                and self.statements == other.statements
                and self.elseStatements == other.elseStatements)

class WhileNode:
    def __init__(self, conditional, statements):
        self.conditional = conditional
        self.statements = statements

    def __repr__(self):
        return "WhileNode(conditional = '{}', statements = '{}')".format(self.conditional, self.statements)

    def __eq__(self, other):
        return (isinstance(other, WhileNode)
                and self.conditional == other.conditional
                and self.statements == other.statements)

class IdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "IdentifierNode(value = '{}')".format(self.value)

    def __eq__(self, other):
        return (isinstance(other, IdentifierNode)
                and self.value == other.value)

class VariableNode:
    def __init__(self, identifier, _type):
        self.identifier = identifier
        self._type = _type

    def __repr__(self):
        return "VariableNode(identifier = '{}', type = '{}')".format(self.identifier, self._type)

    def __eq__(self, other):
        return (isinstance(other, VariableNode)
                and self.identifier == other.identifier
                and self._type == other._type)

class AssignmentNode:
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return "AssignmentNode(variable = '{}', expression = '{}')".format(self.variable, self.expression)

    def __eq__(self, other):
        return (isinstance(other, AssignmentNode)
                and self.variable == other.variable
                and self.expression == other.expression)

class FunctionNode:
    def __init__(self, name, _type, parameters, statements):
        self.name = name
        self._type = _type
        self.parameters = parameters
        self.statements = statements

    def __repr__(self):
        return "FunctionNode(name = '{}', type = '{}', parameters = '{}', statements = '{}')".format(self.name, self._type, self.parameters, self.statements)

    def __eq__(self, other):
        return (isinstance(other, FunctionNode)
            and self.name == other.name
            and self._type == other._type
            and self.parameters == other.parameters
            and self.statements == other.statements)

class ReturnNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "ReturnNode(value = '{}')".format(self.value)

    def __eq__(self, other):
        return (isinstance(other, ReturnNode)
                and self.value == other.value)

class Parser:
    def __init__(self, tokens, originalString):
        self.originalString = originalString
        self.tokens = tokens
        self.buffer = ArrayBuffer(tokens)

    def parse(self):
        nodes = []
        while self.buffer.remaining() > 0:
            nodes.append(self.parseTopLevel())
        return nodes

    def parseTopLevel(self):
        peekToken = self.buffer.peek()
        if peekToken.match("identifier", "func"):
            return self.parseFunction()
        else:
            return self.parseAssignment()

    def parseStatement(self):
        peekToken = self.buffer.peek()
        if peekToken.match("identifier", "if"):
            return self.parseIf()
        elif peekToken.match("identifier", "while"):
            return self.parseWhile()
        elif peekToken.match("identifier", "return"):
            return self.parseReturn()
        else:
            callOrIdentifierNode = self.parseCallOrIdentifier()
            if isinstance(callOrIdentifierNode, CallNode):
                self.requireToken("syntax", ";")
                return callOrIdentifierNode
            else:
                return self.parseAssignmentFromIdentifier(callOrIdentifierNode)

    def parseAssignment(self):
        identifierToken = self.requireToken("identifier", None)
        identifierNode = IdentifierNode(identifierToken.value)
        return self.parseAssignmentFromIdentifier(identifierNode)

    def parseAssignmentFromIdentifier(self, identifierNode):
        variableNode = self.parseVariableFromIdetifier(identifierNode)
        self.requireToken("syntax", "=")
        expressionNode = self.parseExpression()
        self.requireToken("syntax", ";")
        return AssignmentNode(variableNode, expressionNode)

    def parseFunction(self):
        self.requireToken("identifier", "func")
        nameIdentifierToken = self.requireToken("identifier", None, "Name is missing.")
        self.requireToken("syntax", "(")
        parameterNodes = []
        if not self.buffer.peek().match("syntax", ")"):
            parameterNodes.append(self.parseVariable())
            while True:
                peekToken = self.buffer.peek()
                if peekToken is not None and peekToken.match("syntax", ","):
                    self.buffer.consume()
                    parameterNodes.append(self.parseVariable())
                else:
                    break
        self.requireToken("syntax", ")")
        self.requireToken("syntax", ":")
        typeIdentifierToken = self.requireToken("identifier", None, "Type is missing.")
        statements = self.parseStatementBlock()
        return FunctionNode(
            IdentifierNode(nameIdentifierToken.value),
            IdentifierNode(typeIdentifierToken.value),
            parameterNodes,
            statements
        )

    def parseWhile(self):
        whileToken = self.buffer.consume()
        conditional = self.parseExpression()
        statements = self.parseStatementBlock()
        return WhileNode(conditional, statements)

    def parseIf(self):
        ifToken = self.buffer.consume()
        conditional = self.parseExpression()
        statements = self.parseStatementBlock()
        elseStatements = []
        peekToken = self.buffer.peek()
        if peekToken is not None and peekToken.match("identifier", "else"):
            self.buffer.consume()
            elseStatements = self.parseStatementBlock()
        return IfNode(conditional, statements, elseStatements)

    def parseReturn(self):
        self.requireToken("identifier", "return")
        peekToken = self.buffer.peek()
        expression = None
        if not peekToken.match("syntax", ";"):
            expression = self.parseExpression()
        self.requireToken("syntax", ";")
        return ReturnNode(expression)

    def parseStatementBlock(self):
        self.requireToken("syntax", "{")
        statements = []
        while self.buffer.remaining() > 0 and not self.buffer.peek().match("syntax", "}"):
            statements.append(self.parseStatement())
        self.requireToken("syntax", "}")
        return statements

    def parseExpression(self):
        left = self.parseInfixL1()
        opToken = self.buffer.peek()
        if opToken is not None and opToken.matchList("syntax", ["!=", "=="]):
            self.buffer.consume()
            right = self.parseInfixL1()
            return InfixNode(left, opToken.value, right)
        else:
            return left

    def parseInfixL1(self):
        left = self.parseInfixL2()
        opToken = self.buffer.peek()
        if opToken is not None and opToken.matchList("syntax", ["+", "-"]):
            self.buffer.consume()
            right = self.parseInfixL2()
            return InfixNode(left, opToken.value, right)
        else:
            return left

    def parseInfixL2(self):
        left = self.parsePrefix()
        opToken = self.buffer.peek()
        if opToken is not None and opToken.matchList("syntax", ["*", "/"]):
            self.buffer.consume()
            right = self.parsePrefix()
            return InfixNode(left, opToken.value, right)
        else:
            return left

    def parsePrefix(self):
        prefix = None
        right = None
        peekToken = self.buffer.peek()
        if peekToken is None:
            return None
        if peekToken.matchList("syntax", ["-"]):
            token = self.buffer.consume()
            prefix = token.value
            peekToken = self.buffer.peek()

        if peekToken is None:
            return None
        if peekToken.matchType("numberLiteral"):
            token = self.buffer.consume()
            right = NumberLiteralNode(token.value)
        elif peekToken.match("syntax", "("):
            self.buffer.consume()
            right = self.parseExpression()
            self.requireToken("syntax", ")")
        else:
            right = self.parseCallOrIdentifier()

        if prefix is None:
            return right
        else:
            return PrefixNode(prefix, right)

    def parseCallOrIdentifier(self):
        identifierToken = self.requireToken("identifier", None)
        identifierNode = IdentifierNode(identifierToken.value)
        peekToken = self.buffer.peek()
        if peekToken.match("syntax", "("):
            self.buffer.consume()
            argumentNodes = []
            if not self.buffer.peek().match("syntax", ")"):
                argumentNodes.append(self.parseExpression())
                while True:
                    argPeekToken = self.buffer.peek()
                    if argPeekToken is not None and argPeekToken.match("syntax", ","):
                        self.buffer.consume()
                        argumentNodes.append(self.parseExpression())
                    else:
                        break
            self.requireToken("syntax", ")")
            return CallNode(identifierNode, argumentNodes)
        else:
            return identifierNode

    def parseVariable(self):
        identifierToken = self.requireToken("identifier", None)
        identifierNode = IdentifierNode(identifierToken.value)
        return self.parseVariableFromIdetifier(identifierNode)

    def parseVariableFromIdetifier(self, identifierNode):
        self.requireToken("syntax", ":", "Missing ':' before type.")
        typeIdentifierToken = self.requireToken("identifier", None)
        typeIdentifierNode = IdentifierNode(typeIdentifierToken.value)
        return VariableNode(identifierNode, typeIdentifierNode)

    def requireToken(self, _type, value, additionalDetails = ""):
        peekToken = self.buffer.peek()
        if peekToken is None or not ((value is None and peekToken.matchType(_type)) or peekToken.match(_type, value)):
            missing = value
            if missing is None:
                missing = _type
            displayError(self.originalString, self.buffer.lookback().pos, "Detected a missing '{}'. {}".format(missing, additionalDetails))
            raise
        self.buffer.consume()
        return peekToken
