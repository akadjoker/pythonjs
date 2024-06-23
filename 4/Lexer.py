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
            self.add_token(TokenType.POWER)
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
        text = self.source[self.start:self.current].lower()
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
        elif text == 'elif':
            self.add_token(TokenType.ELIF)
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
        elif text == 'for':
            self.add_token(TokenType.FOR)
        elif text == 'break':
            self.add_token(TokenType.BREAK) 
        elif text == 'continue':
            self.add_token(TokenType.CONTINUE)
        elif text == 'goto':
            self.add_token(TokenType.GOTO)
        elif text == 'eval':
            self.add_token(TokenType.EVAL)
        elif text == 'now':
            self.add_token(TokenType.NOW)
        elif text == 'program':
            self.add_token(TokenType.PROGRAM)
        elif text == 'process':
            self.add_token(TokenType.PROCESS)
        elif text == 'import':
            self.add_token(TokenType.IMPORT)
        elif text == 'frame':
            self.add_token(TokenType.FRAME)
        elif text == 'start':
            self.add_token(TokenType.START)
        elif text == 'func':
            self.add_token(TokenType.FUNCTION)
        elif text == 'proc':
            self.add_token(TokenType.PROCEDURE)
        elif text == 'struct':
            self.add_token(TokenType.STRUCT)
        elif text == 'switch':
            self.add_token(TokenType.SWITCH)
        elif text == 'case':
            self.add_token(TokenType.CASE)
        elif text == 'default':
            self.add_token(TokenType.DEFAULT)
        elif text == 'loop':
            self.add_token(TokenType.LOOP)
        elif text == 'and':
            self.add_token(TokenType.AND)
        elif text == 'or':
            self.add_token(TokenType.OR)
        elif text == 'not':
            self.add_token(TokenType.BANG)
        elif text == 'xor':
            self.add_token(TokenType.XOR)
        elif text == 'mod':
            self.add_token(TokenType.MOD)
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
