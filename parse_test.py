import unittest
from parse import *
from lex import *

class TestParse(unittest.TestCase):
    def testBasicExpression(self):
        originalString = "1 + 1"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected = InfixNode(NumberLiteralNode(1), "+", NumberLiteralNode(1))
        self.assertEqual(actual, expected)

    def testOrderOfOperations(self):
        originalString = "1 + 2 * 3"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected = InfixNode(
            NumberLiteralNode(1),
            "+",
            InfixNode(
                NumberLiteralNode(2),
                "*",
                NumberLiteralNode(3)
            )
        )
        self.assertEqual(actual, expected)

    def testOrderOfOperationsWithParens(self):
        originalString = "(1 + 2) * 3"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected =InfixNode(
            InfixNode(
                NumberLiteralNode(1),
                "+",
                NumberLiteralNode(2)
            ),
            "*",
            NumberLiteralNode(3)
        )
        self.assertEqual(actual, expected)

    def testCall(self):
        originalString = "1 + someCall(1 + 1, 2)"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected = InfixNode(
            NumberLiteralNode(1),
            "+",
            CallNode(
                IdentifierNode("someCall"),
                [
                    InfixNode(NumberLiteralNode(1), "+", NumberLiteralNode(1)),
                    NumberLiteralNode(2)
                ]
            )
        )
        self.assertEqual(actual, expected)

    def testIf(self):
        originalString = "if 1 { myFun(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = IfNode(NumberLiteralNode(1), [CallNode(IdentifierNode("myFun"), [])], [])
        self.assertEqual(actual, expected)

    def testIfElse(self):
        originalString = "if 1 { myFun(); } else { myFun2(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = IfNode(NumberLiteralNode(1), [CallNode(IdentifierNode("myFun"), [])], [CallNode(IdentifierNode("myFun2"), [])])
        self.assertEqual(actual, expected)

    def testWhile(self):
        originalString = "while 1 { myFun(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = WhileNode(NumberLiteralNode(1), [CallNode(IdentifierNode("myFun"), [])])
        self.assertEqual(actual, expected)

    def testParseVariable(self):
        originalString = "myNum : int = 1;"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = AssignmentNode(VariableNode(IdentifierNode("myNum"), IdentifierNode("int")), NumberLiteralNode(1))
        self.assertEqual(actual, expected)

    def testParseFullProgram(self):
        originalString = """
        myNum: int = 1;
        func myFunction(x: int): int {
            if x == myNum {
                return 1;
            } else {
                return 0;
            }
        }
        """
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parse()
        expected = [
                AssignmentNode(VariableNode(IdentifierNode("myNum"), IdentifierNode("int")), NumberLiteralNode(1)),
                FunctionNode(
                    IdentifierNode("myFunction"),
                    IdentifierNode("int"),
                    [VariableNode(IdentifierNode("x"), IdentifierNode("int"))],
                    [
                        IfNode(
                            InfixNode(IdentifierNode("x"), "==", IdentifierNode("myNum")),
                            [ReturnNode(NumberLiteralNode(1))],
                            [ReturnNode(NumberLiteralNode(0))]
                        )
                    ]
                )
        ]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
