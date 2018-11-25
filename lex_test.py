import unittest
from lex import *

class TestLex(unittest.TestCase):
    def testSimpleExpression(self):
        lexxer = Lexxer("if (10 + mynum2 == 12)")
        actual = lexxer.lex()
        expected = [
            Token("syntax", "if", (0, 1)),
            Token("syntax", "(", (0, 3)),
            Token("numberLiteral", 10, (0, 5)),
            Token("syntax", "+", (0, 7)),
            Token("identifier", "mynum2", (0, 14)),
            Token("syntax", "==", (0, 17)),
            Token("numberLiteral", 12, (0, 20)),
            Token("syntax", ")", (0, 21)),
        ]

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
