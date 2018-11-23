import unittest
from parse import *
from lex import *

class TestParse(unittest.TestCase):
    def testBasic(self):
        originalString = "1 + 1\n2 + 2"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parse()
        expected = [
                InfixNode(NumberLiteralNode(1), "+", NumberLiteralNode(1)),
                InfixNode(NumberLiteralNode(2), "+", NumberLiteralNode(2)),
        ]
        self.assertEqual(actual, expected)

    def testOrderOfOperations(self):
        originalString = "1 + 2 * 3"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parse()
        expected = [
                InfixNode(
                    NumberLiteralNode(1),
                    "+",
                    InfixNode(
                        NumberLiteralNode(2),
                        "*",
                        NumberLiteralNode(3)
                    )
                )
        ]
        self.assertEqual(actual, expected)

    def testOrderOfOperationsWithParens(self):
        originalString = "(1 + 2) * 3"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parse()
        expected = [
                InfixNode(
                    InfixNode(
                        NumberLiteralNode(1),
                        "+",
                        NumberLiteralNode(2)
                    ),
                    "*",
                    NumberLiteralNode(3)
                )
        ]
        self.assertEqual(actual, expected)

    def testCall(self):
        originalString = "1 + someCall(1 + 1, 2)"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parse()
        expected = [
                InfixNode(
                    NumberLiteralNode(1),
                    "+",
                    CallNode(
                        IdentifierNode("someCall"),
                        [
                            InfixNode(NumberLiteralNode(1), "+", NumberLiteralNode(1)),
                            NumberLiteralNode(2)
                        ]
                    )
                ),
        ]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
