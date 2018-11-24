from utils import *

# TODO: simplify the types here

class Token:
    def __init__(self, _type, value, pos):
        self._type = _type
        self.value = value
        self.pos = pos

    def matchType(self, _type):
        return _type == self._type

    def match(self, _type, value):
        return _type == self._type and value == self.value

    def matchList(self, _type, values):
        if _type == self._type:
            for value in values:
                if value == self.value:
                    return True
        return False

    def __eq__(self, other):
        return isinstance(other, Token) and self._type == other._type and self.value == other.value and self.pos == other.pos

    def __repr__(self):
        return "Token(type = '{}', value = '{}', pos = '{}')".format(self._type, self.value, self.pos)

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
                raise
        return tokens

    def lexNumberLiteral(self):
        stringValue = ""
        while self.buffer.remaining() > 0 and isDigit(self.buffer.peek()):
            stringValue += self.buffer.consume()
        numberValue = stringToNumber(stringValue)
        return Token("numberLiteral", numberValue, self.buffer.position())

    def lexIdentifier(self):
        stringValue = ""
        while self.buffer.remaining() > 0 and (isIdentifier(self.buffer.peek()) or isDigit(self.buffer.peek())):
            stringValue += self.buffer.consume()
        return Token("identifier", stringValue, self.buffer.position())
