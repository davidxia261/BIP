class Interpreter:
    def __init__(self):
        self.variables = {}

    def eval(self, node):
        if not node:
            return None
        
        if node[0] == 'num':
            return node[1]
        elif node[0] == 'str':
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
            # If either operand is a string, convert to string and concatenate
                if isinstance(left_val, str) or isinstance(right_val, str):
                    return str(left_val) + str(right_val)
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero") 
                return left_val / right_val
            elif op == '>=':
                return left_val >= right_val
            elif op == '<=':
                return left_val <= right_val
            elif op == '>':
                return left_val > right_val
            elif op == '<':
                return left_val < right_val
            elif op == '==':
                return left_val == right_val
            else:
                raise ValueError(f"Unsupported operator: {op}")
        elif node[0] == 'print':
            result = self.eval(node[1])
            print(result)
            return result
        elif node[0] == 'if':
            condition = self.eval(node[1])
            if condition:
                return self.eval(node[2])  # Execute 'if' body
            elif node[3] is not None:
                return self.eval(node[3])  # Execute 'else' body
            return None
        elif node[0] == 'while':
            condition = node[1]
            body = node[2]
            result = None
            while self.eval(condition):  # Evaluate the condition repeatedly
                if body[0] == 'block':
                    # If body is a block, iterate through its statements
                    for stmt in body[1]:
                        result = self.eval(stmt)
                else:
                    # If body is a single statement
                    result = self.eval(body)
            return result
        elif node[0] == 'block':
            result = None
            for stmt in node[1]:
                result = self.eval(stmt)
            return result
        else:
            raise ValueError(f"Unknown node type: {node[0]}")