class Interpreter:
    def __init__(self):
        self.variables = {}

    def eval(self, node):
        if not node:
            return None
        
        if node[0] == 'num':
            return node[1]
        elif node[0] == 'var':
            var_name = node[1]
            if var_name not in self.variables:
                raise NameError(f"Variable '{var_name}' is not defined")
            return self.variables[var_name]
        elif node[0] == 'assign':
            var_name = node[1]
            expr = node[2]
            value = self.eval(expr)
            self.variables[var_name] = value
            return value
        elif node[0] == 'binop':
            op = node[1]
            left = node[2] 
            right = node[3]
            left_val = self.eval(left)
            right_val = self.eval(right)
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero") 
                return left_val / right_val
        elif node[0] == 'print':
            result = self.eval(node[1])
            print(result)
            return result
        else:
            raise ValueError(f"Unknown node type: {node[0]}")