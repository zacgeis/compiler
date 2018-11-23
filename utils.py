def repeat(char, length):
    string = ""
    for i in range(length):
        string += char
    return string

def stringToNumber(string):
    number = 0
    for char in string:
        number *= 10
        # ord(c) converts a character to its numeric value
        number += ord(char) - ord("0")
    return number

def isDigit(char):
    return char >= "0" and char <= "9"

def isAlpha(char):
    return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z")

def isIdentifier(char):
    return isAlpha(char) or char == "_"

def displayError(string, pos, errorMessage):
    errorLinePos, errorCharPos = pos
    linePos = 0
    line = ""
    for char in string:
        if char == "\n":
            if linePos == errorLinePos:
                break
            line = ""
            linePos += 1
        else:
            line += char
    print()
    print(line)
    print(repeat("-", errorCharPos) + "^")
    print(errorMessage)
    print()

class ArrayBuffer:
    def __init__(self, arr):
        self.i = 0
        self.arr = arr

    def remaining(self):
        return len(self.arr) - self.i

    def peek(self):
        if self.i > len(self.arr) - 1:
            return None

        return self.arr[self.i]

    def consume(self):
        if self.i > len(self.arr) - 1:
            return None

        item = self.arr[self.i]
        self.i += 1
        return item

class TrackedStringBuffer:
    def __init__(self, string):
        self.i = 0
        self.string = string
        self.linePos = 0
        self.charPos = 0

    def remaining(self):
        return len(self.string) - self.i

    def peek(self):
        if self.i > len(self.string) - 1:
            return ""

        return self.string[self.i]

    def consume(self):
        if self.i > len(self.string) - 1:
            return ""

        char = self.string[self.i]
        self.i += 1

        if char == "\n":
            self.linePos += 1
            self.charPos = 0
        else:
            self.charPos += 1

        return char

    def position(self):
        return (self.linePos, self.charPos)

