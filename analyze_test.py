import unittest
from parse import *
from lex import *
from analyze import *

class TestAnalyze(unittest.TestCase):
    # TODO: finish writing this test case
    def testBasic(self):
        originalString = """
        myNum: int = 1;
        func myFunction(x: int): int {
            myLocal: int = 0;
            if x == myNum {
                myLocal = 2;
                return x;
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
        self.assertEqual(False, analyzer.hasErrors())

if __name__ == "__main__":
    unittest.main()
