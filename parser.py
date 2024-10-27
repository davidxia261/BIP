class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if not self.tokens:
            return None
            
        if self.current_token_type() == 'PRINT':
            self.advance() 
            expr = self.expr()
            self.match('END')
            return ('print', expr)
            
        elif self.current_token_type() == 'ID':
            var_name = self.advance()[1]
            if self.current_token_type() == 'ASSIGN':
                self.advance() 
                expr = self.expr()
                self.match('END')
                return ('assign', var_name, expr)
            else:
                self.pos -= 1 
                expr = self.expr()
                self.match('END')
                return expr

        expr = self.expr()
        self.match('END')
        return expr

    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.current_token_type() == 'OP':
            op = self.advance()[1]
            right = self.term()
            node = ('binop', op, node, right)
        return node

    def term(self):
        if self.current_token_type() == 'NUMBER':
            return ('num', self.advance()[1])
        elif self.current_token_type() == 'ID':
            return ('var', self.advance()[1])
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'}")

    def current_token_type(self):
        return self.tokens[self.pos][0] if self.pos < len(self.tokens) else None

    def advance(self):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def match(self, expected_type):
        if self.current_token_type() != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {self.current_token_type()}")
        return self.advance()