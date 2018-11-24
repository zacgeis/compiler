import argparse
from parse import *
from lex import *

def main():
    argparser = argparse.ArgumentParser(description = "Toy compiler")
    argparser.add_argument("file", help = "File to compile")
    args = argparser.parse_args()
    inputFile = open(args.file)
    inputString = inputFile.read()
    lexxer = Lexxer(inputString)
    tokens = lexxer.lex()
    parser = Parser(tokens, inputString)
    nodes = parser.parse()
    print(nodes)

if __name__ == "__main__":
    main()
