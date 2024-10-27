from tokenization import tokenize
from parser import Parser
from interpreter import Interpreter

interpreter = Interpreter()

def run_code(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    tree = parser.parse()
    result = interpreter.eval(tree)
    return result

run_code("x = 10;")
run_code("y = 5;")
run_code("z = x / y;")
run_code("print z;")