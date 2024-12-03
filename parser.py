class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if not self.tokens:
            return None
        statements = []
        while self.pos < len(self.tokens):
            if self.current_token_type() == 'IF':
                statements.append(self.parse_if())    
            elif self.current_token_type() == 'WHILE':
                statements.append(self.parse_while())
            elif self.current_token_type() == 'PRINT':
                self.advance() 
                expr = self.expr()
                self.match('END')
                statements.append(('print', expr))
            elif self.current_token_type() == 'ID':
                var_name = self.advance()[1]
                if self.current_token_type() == 'ASSIGN':
                    self.advance() 
                    expr = self.expr()
                    self.match('END')
                    statements.append(('assign', var_name, expr))
                else:
                    self.pos -= 1 
                    expr = self.expr()
                    self.match('END')
                    statements.append(expr)
            else:
                break
        
        # If only one statement, return it directly
        if len(statements) == 1:
            return statements[0]
        
        # Otherwise, return as a block
        return ('block', statements)


    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.current_token_type() in {'OP', 'COND'}:
            op = self.advance()[1]
            right = self.term()
            node = ('binop', op, node, right)
        return node

    def term(self):
        if self.current_token_type() == 'NUMBER':
            return ('num', self.advance()[1])
        elif self.current_token_type() == 'STRING':
                return ('str', self.advance()[1])  
        elif self.current_token_type() == 'ID':
            return ('var', self.advance()[1])
        elif self.current_token_type() in {'IF', 'ELSE', 'WHILE', 'PRINT'}:
            # Skip keywords if encountered unexpectedly
            self.advance()
            return self.term()
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
    
    def parse_block(self):
        statements = []
        while self.pos < len(self.tokens) and self.current_token_type() not in {'END', 'ELSE', 'RPAREN'}:
            statements.append(self.parse())
        return ('block', statements) if len(statements) > 1 else statements[0]

    def parse_if(self):
        self.match('IF')  # Consume 'if'
        self.match('LPAREN')  # Consume '('
        condition = self.expr()  # Parse condition
        self.match('RPAREN')  # Consume ')'
        body = self.parse_block()  # Parse the body of the 'if'
        else_body = None
        if self.current_token_type() == 'ELSE':
            self.advance()  # Consume 'else'
            else_body = self.parse_block()  # Parse the body of the 'else'
        return ('if', condition, body, else_body)
    
    def parse_while(self):
        self.match('WHILE')  # Consume 'while'
        self.match('LPAREN')  # Consume '('
        condition = self.expr()  # Parse condition
        self.match('RPAREN')  # Consume ')'
        body = self.parse_block()
        return ('while', condition, body)