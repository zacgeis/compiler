from utils import *

class LiteralNode:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __repr__(self):
        return "LiteralNode(type = '{}', value = '{}')".format(self.type, self.value)

    def __eq__(self, other):
        return (isinstance(other, LiteralNode)
                and self.type == other.type
                and self.value == other.value)

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

class DeclarationNode:
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return "DeclarationNode(variable = '{}', expression = '{}')".format(self.variable, self.expression)

    def __eq__(self, other):
        return (isinstance(other, DeclarationNode)
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
        if peekToken.match("syntax", "func"):
            return self.parseFunction()
        else:
            declarationNode = self.parseDeclaration()
            self.requireToken("syntax", ";")
            return declarationNode

    def parseStatement(self):
        peekToken = self.buffer.peek()
        if peekToken.match("syntax", "if"):
            return self.parseIf()
        elif peekToken.match("syntax", "while"):
            return self.parseWhile()
        elif peekToken.match("syntax", "return"):
            return self.parseReturn()
        else:
            identifierToken = self.requireToken("identifier", None)
            node = None
            if self.buffer.peek().match("syntax", "("):
                node = self.parseCall(identifierToken)
            elif self.buffer.peek().match("syntax", ":"):
                node = self.parseDeclarationFromIdentifier(identifierToken)
            else:
                self.requireToken("syntax", "=")
                expression = self.parseExpression()
                # = is a call node for now. if, while, and func all have an impact on the assembly structure. = does not.
                node = CallNode("=", [IdentifierNode(identifierToken.value), expression])
            self.requireToken("syntax", ";")
            return node

    def parseDeclaration(self):
        identifierToken = self.requireToken("identifier", None)
        return self.parseDeclarationFromIdentifier(identifierToken)

    def parseDeclarationFromIdentifier(self, identifierToken):
        variableNode = self.parseVariableFromIdentifier(identifierToken)
        self.requireToken("syntax", "=")
        expressionNode = self.parseExpression()
        return DeclarationNode(variableNode, expressionNode)

    def parseFunction(self):
        self.requireToken("syntax", "func")
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
            nameIdentifierToken.value,
            typeIdentifierToken.value,
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
        if peekToken is not None and peekToken.match("syntax", "else"):
            self.buffer.consume()
            elseStatements = self.parseStatementBlock()
        return IfNode(conditional, statements, elseStatements)

    def parseReturn(self):
        self.requireToken("syntax", "return")
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
            return CallNode(opToken.value, [left, right])
        else:
            return left

    def parseInfixL1(self):
        left = self.parseInfixL2()
        opToken = self.buffer.peek()
        if opToken is not None and opToken.matchList("syntax", ["+", "-"]):
            self.buffer.consume()
            right = self.parseInfixL2()
            return CallNode(opToken.value, [left, right])
        else:
            return left

    def parseInfixL2(self):
        left = self.parsePrefix()
        opToken = self.buffer.peek()
        if opToken is not None and opToken.matchList("syntax", ["*", "/"]):
            self.buffer.consume()
            right = self.parsePrefix()
            return CallNode(opToken.value, [left, right])
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
            right = LiteralNode("integer", token.value)
        elif peekToken.match("syntax", "("):
            self.buffer.consume()
            right = self.parseExpression()
            self.requireToken("syntax", ")")
        else:
            identifierToken = self.requireToken("identifier", None)
            if self.buffer.peek().match("syntax", "("):
                right = self.parseCall(identifierToken)
            else:
                right = IdentifierNode(identifierToken.value)

        if prefix is None:
            return right
        else:
            return CallNode(prefix, [right])

    def parseCall(self, identifierToken):
        self.requireToken("syntax", "(")
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
        return CallNode(identifierToken.value, argumentNodes)

    def parseVariable(self):
        identifierToken = self.requireToken("identifier", None)
        return self.parseVariableFromIdentifier(identifierToken)

    def parseVariableFromIdentifier(self, identifierToken):
        self.requireToken("syntax", ":", "Missing ':' before type.")
        typeIdentifierToken = self.requireToken("identifier", None)
        return VariableNode(identifierToken.value, typeIdentifierToken.value)

    def requireToken(self, _type, value, additionalDetails = ""):
        peekToken = self.buffer.peek()
        if peekToken is None or not ((value is None and peekToken.matchType(_type)) or peekToken.match(_type, value)):
            missing = value
            if missing is None:
                missing = _type
            displayError(self.originalString, self.buffer.lookback().pos, "Detected a missing '{}'. {}".format(missing, additionalDetails))
            raise
        return self.buffer.consume()

    def requireTokens(self, type_value_pairs, additionalDetails = ""):
        peekToken = self.buffer.peek()
        matched = False
        matchedToken = None
        values = []
        for _type, value in type_value_pairs:
            if peekToken.match(_type, value):
                matched = True
                matchedToken = self.buffer.consume()
                break
            values.append(value)
        if not matched:
            displayError(
                    self.originalString,
                    self.buffer.lookback().pos,
                    "Detected a missing '{}'. {}".format("' or '".join(values), additionalDetails)
            )
            raise
        return matchedToken
