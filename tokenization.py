import re

# Define the tokens
token_specification = [
    ('NUMBER', r'\d+(\.\d*)?'),   # Integer or decimal number
    ('ASSIGN', r'='),             # Assignment operator
    ('END', r';'),                # Statement terminator
    ('ID', r'[A-Za-z]+'),         # Identifiers
    ('OP', r'[+\-*/]'),           # Arithmetic operators
    ('SKIP', r'[ \t]+'),          # Skip whitespace
    ('MISMATCH', r'.'),           # Any other character
]

# Build the regex pattern
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

# Tokenizer function
def tokenize(code):
    tokens = []
    pos = 0
    match = get_token(code)
    while match:
        type = match.lastgroup
        value = match.group(type)
        if type == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif type == 'ID' and value == 'print':
            type = 'PRINT'
        if type != 'SKIP':
            tokens.append((type, value))
        pos = match.end()
        match = get_token(code, pos)
    if pos != len(code):
        raise SyntaxError(f"Unexpected character '{code[pos]}' at position {pos}")
    return tokens