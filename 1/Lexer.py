from Token import Token, TokenType

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1

    def tokenize(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "EOF", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scan_token(self):
        char = self.advance()
        if char == ' ' or char == '\r' or char == '\t':
            pass
        elif char == '\n':
            self.line += 1
        elif char.isdigit() or char == '.':
            self.number()
        elif char == '"':
            self.string()
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif char == '<':
            if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif char == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif char == '*':
            self.add_token(TokenType.STAR)
        elif char == '/':
            if self.match('/'):
                self.line_comment()
            elif self.match('*'):
                self.block_comment()
            else:
                self.add_token(TokenType.SLASH)
        elif char == '%':
            self.add_token(TokenType.PERCENT)
        elif char == '^':
            self.add_token(TokenType.CARET)
        elif char == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '(':
            self.add_token(TokenType.LPAREN)
        elif char == ')':
            self.add_token(TokenType.RPAREN)
        elif char == '{':
            self.add_token(TokenType.LBRACE)
        elif char == '}':
            self.add_token(TokenType.RBRACE)
        elif char == '[':
            self.add_token(TokenType.LBRACKET)
        elif char == ']':
            self.add_token(TokenType.RBRACKET)
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '#':
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()       
        elif char == ':':
            self.add_token(TokenType.COLON)     
        elif char == '.':
            self.add_token(TokenType.DOT)
        elif char == '&':
            self.add_token(TokenType.AND)
        elif char == '|':
            self.add_token(TokenType.OR)
        elif char == 'b' and self.match('reak'):
            self.add_token(TokenType.BREAK)
        elif char == 'c' and self.match('ontinue'):
            self.add_token(TokenType.CONTINUE)
        elif char == 'a' and self.match('nd'):
            self.add_token(TokenType.AND)
        elif char == 'e' and self.match('val'):
            self.add_token(TokenType.EVAL)
        elif char == 'o' and self.match('r'):
            self.add_token(TokenType.OR)
        elif char == 'g' and self.match('oto'):
            self.add_token(TokenType.GOTO)
        elif char == 'p' and self.match('rocess'):
            self.add_token(TokenType.PROCESS)
        elif char == 'f' and self.match('unction'):
            self.add_token(TokenType.FUNCTION)
        elif char == 'e' and self.match('lse'):
            self.add_token(TokenType.ELSE)
        elif char == 'p' and self.match('rint'):
            self.add_token(TokenType.PRINT)
        elif char == 's' and self.match('truct'):
            self.add_token(TokenType.STRUCT)
        elif char == 'i' and self.match('f'):
            self.add_token(TokenType.IF)
        elif char == 'e' and self.match('lseif'):            
            self.add_token(TokenType.ELSEIF)
        elif char == 'w' and self.match('hile'):
            self.add_token(TokenType.WHILE)
        elif char == 'd' and self.match('o'):
            self.add_token(TokenType.DO)
        elif char == 'r' and self.match('eturn'):
            self.add_token(TokenType.RETURN)
        elif char == 'n' and self.match('il'):
            self.add_token(TokenType.NIL)
        elif char == 't' and self.match('rue'):
            self.add_token(TokenType.TRUE)
        elif char == 'f' and self.match('alse'):
            self.add_token(TokenType.FALSE)
        elif char == 'x' and self.match('or'):
            self.add_token(TokenType.XOR)
        elif char == 'a' and self.match('nd'):
            self.add_token(TokenType.AND)
        elif char == 'n' and self.match('ot'):
            self.add_token(TokenType.NOT)
        elif char == 'm' and self.match('od'):
            self.add_token(TokenType.MOD)
        elif char == 'p' and self.match('ow'):
            self.add_token(TokenType.POW)  
        elif char == 'p' and self.match('rogram'):
            self.add_token(TokenType.PROGRAM)
        elif char == 'i' and self.match('nt'):
            self.add_token(TokenType.IDINT)
        elif char == 'b' and self.match('ool'):
            self.add_token(TokenType.IDBOOL)
        elif char == 'f' and self.match('loat'):
            self.add_token(TokenType.IDFLOAT)
        elif char == 's' and self.match('tring'):
            self.add_token(TokenType.IDSTRING)
        elif char.isalpha():
            self.identifier()
        else:
            raise Exception(f"Unexpected character: {char} at line: {self.line}")

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current:self.current+len(expected)] != expected:
            return False
        self.current += len(expected)
        return True

    def number(self):
        isFloat = False
        while self.peek().isdigit() or (self.peek() == '.'):
            if self.peek() == '.':
                isFloat = True
            self.advance()
        if isFloat:
            self.add_token(TokenType.FLOAT, float(self.source[self.start:self.current]))
        else:
            self.add_token(TokenType.INTEGER, int(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise Exception("Unterminated string " + " at line: " + str(self.line))
        self.advance()  
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        if text == 'int':
            self.add_token(TokenType.IDINT)
        elif text == 'float':
            self.add_token(TokenType.IDFLOAT)
        elif text == 'string':
            self.add_token(TokenType.IDSTRING)
        elif text == 'bool':
            self.add_token(TokenType.IDBOOL)
        elif text == 'process':
            self.add_token(TokenType.PROCESS)
        elif text == 'function':
            self.add_token(TokenType.FUNCTION)
        elif text == 'else':
            self.add_token(TokenType.ELSE)
        elif text == 'print':
            self.add_token(TokenType.PRINT)
        elif text == 'struct':
            self.add_token(TokenType.STRUCT)
        elif text == 'if':
            self.add_token(TokenType.IF)
        elif text == 'elseif':
            self.add_token(TokenType.ELSEIF)
        elif text == 'while':
            self.add_token(TokenType.WHILE)
        elif text == 'do':
            self.add_token(TokenType.DO)
        elif text == 'return':
            self.add_token(TokenType.RETURN)
        elif text == 'nil':
            self.add_token(TokenType.NIL)
        elif text == 'true':
            self.add_token(TokenType.TRUE)
        elif text == 'false':
            self.add_token(TokenType.FALSE)
        elif text == 'xor':
            self.add_token(TokenType.XOR)
        elif text == 'and':
            self.add_token(TokenType.AND)
        elif text == 'not':
            self.add_token(TokenType.NOT)
        elif text == 'mod':
            self.add_token(TokenType.MOD)
        elif text == 'pow':
            self.add_token(TokenType.POW)
        else:
            self.add_token(TokenType.IDENTIFIER, text)

    def line_comment(self):
        while self.peek() != '\n' and not self.is_at_end():
            self.advance()

    def block_comment(self):
        while not (self.peek() == '*' and self.peek_next() == '/') and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise Exception("Unterminated block comment at line: " + str(self.line))
        self.advance()  # Consume '*'
        self.advance()  # Consume '/'

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
