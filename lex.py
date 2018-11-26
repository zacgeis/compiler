from utils import *

# TODO: simplify the types here

SYNTAX_IDENTIFIERS = ["func", "if", "else", "while", "return"]

class Token:
    def __init__(self, _type, value, pos):
        self.type = _type
        self.value = value
        self.pos = pos

    def matchType(self, _type):
        return _type == self.type

    def match(self, _type, value):
        return _type == self.type and value == self.value

    def matchList(self, _type, values):
        if _type == self.type:
            for value in values:
                if value == self.value:
                    return True
        return False

    def isLiteral(self):
        return (self.type == "integerLiteral"
                or self.type == "stringLiteral")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.type == other.type and self.value == other.value and self.pos == other.pos

    def __repr__(self):
        return "Token(type = '{}', value = '{}', pos = '{}')".format(self.type, self.value, self.pos)

class Lexxer:
    def __init__(self, originalString):
        self.originalString = originalString
        self.buffer = TrackedStringBuffer(originalString)

    def lex(self):
        tokens = []
        while self.buffer.remaining() > 0:
            peek = self.buffer.peek()
            if peek == " ":
                self.buffer.consume()
            elif peek == "\n":
                self.buffer.consume()
            elif peek == "{":
                self.buffer.consume()
                tokens.append(Token("syntax", "{", self.buffer.position()))
            elif peek == "}":
                self.buffer.consume()
                tokens.append(Token("syntax", "}", self.buffer.position()))
            elif peek == "(":
                self.buffer.consume()
                tokens.append(Token("syntax", "(", self.buffer.position()))
            elif peek == ")":
                self.buffer.consume()
                tokens.append(Token("syntax", ")", self.buffer.position()))
            elif peek == ":":
                self.buffer.consume()
                tokens.append(Token("syntax", ":", self.buffer.position()))
            elif peek == ";":
                self.buffer.consume()
                tokens.append(Token("syntax", ";", self.buffer.position()))
            elif peek == ",":
                self.buffer.consume()
                tokens.append(Token("syntax", ",", self.buffer.position()))
            elif peek == "=":
                self.buffer.consume()
                if self.buffer.peek() == "=":
                    self.buffer.consume()
                    tokens.append(Token("syntax", "==", self.buffer.position()))
                else:
                    tokens.append(Token("syntax", "=", self.buffer.position()))
            elif peek == "+":
                self.buffer.consume()
                tokens.append(Token("syntax", "+", self.buffer.position()))
            elif peek == "-":
                self.buffer.consume()
                tokens.append(Token("syntax", "-", self.buffer.position()))
            elif peek == "*":
                self.buffer.consume()
                tokens.append(Token("syntax", "*", self.buffer.position()))
            elif peek == "/":
                self.buffer.consume()
                tokens.append(Token("syntax", "/", self.buffer.position()))
            elif peek == "!":
                self.buffer.consume()
                if self.buffer.peek() == "=":
                    self.buffer.consume()
                    tokens.append(Token("syntax", "!=", self.buffer.position()))
                else:
                    tokens.append(Token("syntax", "!", self.buffer.position()))
            elif isDigit(peek):
                tokens.append(self.lexNumberLiteral())
            elif isIdentifier(peek):
                tokens.append(self.lexIdentifier())
            else:
                displayError(self.originalString, self.buffer.position(), "Unexpected token: '{}'.".format(peek))
                raise Exception("Syntax error")
        return tokens

    # TODO: eventually this will support more than integers -- floats, etc
    def lexNumberLiteral(self):
        stringValue = ""
        while self.buffer.remaining() > 0 and isDigit(self.buffer.peek()):
            stringValue += self.buffer.consume()
        numberValue = stringToNumber(stringValue)
        return Token("integerLiteral", numberValue, self.buffer.position())

    def lexIdentifier(self):
        stringValue = ""
        while self.buffer.remaining() > 0 and (isIdentifier(self.buffer.peek()) or isDigit(self.buffer.peek())):
            stringValue += self.buffer.consume()
        # Doing this for the potential of better syntax highlighting
        _type = "identifier"
        if stringValue in SYNTAX_IDENTIFIERS:
            _type = "syntax"
        return Token(_type, stringValue, self.buffer.position())
