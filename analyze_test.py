import unittest
from parse import *
from lex import *
from analyze import *

class TestAnalyze(unittest.TestCase):
    def testBasic(self):
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
        nodes = parser.parse()
        analyzer = Analyzer(nodes, originalString)
        analyzer.analyze()
        self.assertEqual(True, True)

if __name__ == "__main__":
    unittest.main()
