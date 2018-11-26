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
        expected = CallNode("+", [LiteralNode("int", 1), LiteralNode("int", 1)])
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
                LiteralNode("int", 1),
                CallNode("*", [LiteralNode("int", 2), LiteralNode("int", 3)])
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
                CallNode("+", [LiteralNode("int", 1), LiteralNode("int", 2)]),
                LiteralNode("int", 3)
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
                LiteralNode("int", 1),
                CallNode(
                    "someCall",
                    [
                        CallNode("+", [LiteralNode("int", 1), LiteralNode("int", 1)]),
                        LiteralNode("int", 2)
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
        expected = IfNode(LiteralNode("int", 1), [CallNode("myFun", [])], [])
        self.assertEqual(actual, expected)

    def testIfElse(self):
        originalString = "if 1 { myFun(); } else { myFun2(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = IfNode(LiteralNode("int", 1), [CallNode("myFun", [])], [CallNode("myFun2", [])])
        self.assertEqual(actual, expected)

    def testWhile(self):
        originalString = "while 1 { myFun(); }"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = WhileNode(LiteralNode("int", 1), [CallNode("myFun", [])])
        self.assertEqual(actual, expected)

    def testParseVariable(self):
        originalString = "myNum : int = 1;"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseStatement()
        expected = DeclarationNode(VariableNode("myNum","int"), LiteralNode("int", 1))
        self.assertEqual(actual, expected)

    def testReturn(self):
        originalString = "return 1 + 2 + 3;"
        lexxer = Lexxer(originalString)
        tokens = lexxer.lex()
        parser = Parser(tokens, originalString)
        actual = parser.parseReturn()
        expected = ReturnNode(
                CallNode(
                    "+",
                    [
                        LiteralNode("int", 1),
                        CallNode("+", [LiteralNode("int", 2), LiteralNode("int", 3)])
                    ]
                )
        )
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
                GlobalDeclarationNode(VariableNode("myNum", "int"), LiteralNode("int", 1)),
                FunctionNode(
                    "myFunction",
                    "int",
                    [VariableNode("x", "int")],
                    [
                        DeclarationNode(VariableNode("myLocal", "int"), LiteralNode("int", 0)),
                        IfNode(
                            CallNode("==", [IdentifierNode("x"), IdentifierNode("myNum")]),
                            [
                                CallNode("=", [IdentifierNode("myLocal"), LiteralNode("int", 2)]),
                                ReturnNode(LiteralNode("int", 1))
                            ],
                            [ReturnNode(LiteralNode("int", 0))]
                        )
                    ]
                )
        ]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
