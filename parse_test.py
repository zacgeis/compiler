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
        expected = CallNode("+", [LiteralNode("integer", 1), LiteralNode("integer", 1)])
        self.assertEqual(actual, expected)

    def testOrderOfOperations(self):
        originalString = "1 + 2 * 3"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected = CallNode(
            "+",
            [
                LiteralNode("integer", 1),
                CallNode("*", [LiteralNode("integer", 2), LiteralNode("integer", 3)])
            ]
        )
        self.assertEqual(actual, expected)

    def testOrderOfOperationsWithParens(self):
        originalString = "(1 + 2) * 3"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected = CallNode(
            "*",
            [
                CallNode("+", [LiteralNode("integer", 1), LiteralNode("integer", 2)]),
                LiteralNode("integer", 3)
            ]
        )
        self.assertEqual(actual, expected)

    def testCall(self):
        originalString = "1 + someCall(1 + 1, 2)"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseExpression()
        expected = CallNode(
            "+",
            [
                LiteralNode("integer", 1),
                CallNode(
                    "someCall",
                    [
                        CallNode("+", [LiteralNode("integer", 1), LiteralNode("integer", 1)]),
                        LiteralNode("integer", 2)
                    ]
                )
            ]
        )
        self.assertEqual(actual, expected)

    def testIf(self):
        originalString = "if 1 { myFun(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = IfNode(LiteralNode("integer", 1), [CallNode("myFun", [])], [])
        self.assertEqual(actual, expected)

    def testIfElse(self):
        originalString = "if 1 { myFun(); } else { myFun2(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = IfNode(LiteralNode("integer", 1), [CallNode("myFun", [])], [CallNode("myFun2", [])])
        self.assertEqual(actual, expected)

    def testWhile(self):
        originalString = "while 1 { myFun(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = WhileNode(LiteralNode("integer", 1), [CallNode("myFun", [])])
        self.assertEqual(actual, expected)

    def testParseVariable(self):
        originalString = "myNum : int = 1;"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = DeclarationNode(VariableNode("myNum","int"), LiteralNode("integer", 1))
        self.assertEqual(actual, expected)

    def testParseFullProgram(self):
        originalString = """
        myNum: int = 1;
        func myFunction(x: int): int {
            myLocal: int = 0;
            if x == myNum {
                myLocal = 2;
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
                DeclarationNode(VariableNode("myNum", "int"), LiteralNode("integer", 1)),
                FunctionNode(
                    "myFunction",
                    "int",
                    [VariableNode("x", "int")],
                    [
                        DeclarationNode(VariableNode("myLocal", "int"), LiteralNode("integer", 0)),
                        IfNode(
                            CallNode("==", [IdentifierNode("x"), IdentifierNode("myNum")]),
                            [
                                CallNode("=", [IdentifierNode("myLocal"), LiteralNode("integer", 2)]),
                                ReturnNode(LiteralNode("integer", 1))
                            ],
                            [ReturnNode(LiteralNode("integer", 0))]
                        )
                    ]
                )
        ]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
