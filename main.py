from tokenization import tokenize
from parser import Parser
from interpreter import Interpreter

interpreter = Interpreter()

def run_code(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    tree = parser.parse()
    if tree[0] == 'block':
        result = None
        for stmt in tree[1]:
            result = interpreter.eval(stmt)
        return result
    result = interpreter.eval(tree)
    return result

#Run code here:
run_code('x = 5;')
run_code('y = 2;')
run_code('x = x + y;')
run_code('print "x = " + x;')

#run_code("x = 10;")
#run_code("y = 10;")
#run_code("if (x < y) x = x + 1; else y = y + 1;")
#run_code("print x;")
#run_code("print y;")
#run_code("z = 1; while (z < 3) z = z + 1;")
#run_code("print z;")