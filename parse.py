from utils import *

# See https://github.com/cksystemsteaching/selfie/blob/master/grammar.md

class NumberLiteralNode:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "NumberLiteralNode(number = '{}')".format(self.number)

    def __eq__(self, other):
        return isinstance(other, NumberLiteralNode) and self.number == other.number

class PrefixNode:
    def __init__(self, prefix, right):
        self.prefix = prefix
        self.right = right

    def __repr__(self):
        return "PrefixNode(prefix = '{}', right = '{}')".format(self.prefix, self.right)

    def __eq__(self, other):
        return isinstance(other, PrefixNode) and self.prefix == other.prefix and self.right == other.right

class InfixNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return "InfixNode(left = '{}', op = '{}', right = '{}')".format(self.left, self.op, self.right)

    def __eq__(self, other):
        return isinstance(other, InfixNode) and self.left == other.left and self.op == other.op and self.right == other.right

class CallNode:
    def __init__(self, identifier, arguments2):
        self.identifier = identifier
        self.arguments2 = arguments2

    def __repr__(self):
        return "CallNode(identifier = '{}', arguments2 = '{}')".format(self.identifier, self.arguments2)

    def __eq__(self, other):
        return isinstance(other, CallNode) and self.identifier == other.identifier and self.arguments2 == other.arguments2

class IfNode:
    def __init__(self, conditional, block):
        self.conditional = conditional
        self.statements = statements

    def __repr__(self):
        return "IfNode(conditional = '{}', statements = '{}')".format(self.conditional, self.statements)

    def __eq__(self, other):
        return isinstance(other, IfNode) and self.conditional == other.conditional and self.statements == other.statements

class IdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "IdentifierNode(value = '{}')".format(self.value)

    def __eq__(self, other):
        return isinstance(other, IdentifierNode) and self.value == other.value

class VariableNode:
    def __init__(self, identifier, _type):
        self.identifier = identifier
        self._type = _type

    def __repr__(self):
        return "VariableNode(identifier = '{}', type = '{}')".format(self.identifier, self._type)

    def __eq__(self, other):
        return isinstance(other, VariableNode) and self.identifier == other.identifier and self._type == other._type

class Parser:
    def __init__(self, tokens, originalString):
        self.originalString = originalString
        self.tokens = tokens
        self.buffer = ArrayBuffer(tokens)

    def parse(self):
        nodes = []
        while self.buffer.remaining() > 0:
            nodes.append(self.parseExpression())
        return nodes

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
            closingParen = self.buffer.consume()
            if closingParen is None or not closingParen.match("syntax", ")"):
                self.displayMatchError(peekToken)
                raise
        else:
            right = self.parseCallOrIdentifier()

        if prefix is None:
            return right
        else:
            return PrefixNode(prefix, right)

    def parseCallOrIdentifier(self):
        identifierToken = self.buffer.consume()
        if not identifierToken.matchType("identifier"):
            self.displayError(identifierToken, "Expected identifier here.")
            raise
        identifierNode = IdentifierNode(identifierToken.value)
        peekToken = self.buffer.peek()
        if peekToken.match("syntax", "("):
            self.buffer.consume()
            argumentNodes = []
            argumentNodes.append(self.parseExpression())
            while True:
                argPeekToken = self.buffer.peek()
                if argPeekToken.match("syntax", ","):
                    self.buffer.consume()
                    argumentNodes.append(self.parseExpression())
                else:
                    break
            closingParen = self.buffer.consume()
            if closingParen is None or not closingParen.match("syntax", ")"):
                self.displayMatchError(peekToken)
                raise
            return CallNode(identifierNode, argumentNodes)
        else:
            return identifierNode

    def parseVariable(self):
        identifierToken = self.buffer.consume()
        if not identifierToken.matchType("identifier"):
            self.displayError(identifierToken, "Expected identifier here.")
            raise
        identifierNode = IdentifierNode(identifierToken.value)
        colonToken = self.buffer.consume()
        if not colonToken.match("syntax", ":"):
            self.displayError(identifierToken, "Missing ':' before type.")
        typeIdentifierToken = self.buffer.consume()
        if not typeIdentifierToken.matchType("identifier"):
            self.displayError(typeIdentifierToken, "Expected identifier here.")
            raise
        typeIdentifierNode = IdentifierNode(typeIdentifierToken.value)
        return VariableNode(identifierNode, typeIdentifierNode)

    def displayError(self, token, message):
        displayError(self.originalString, token.pos, message)

    def displayMatchError(self, openToken):
        self.displayError(openToken, "Closing paren not found for this open paren.")
