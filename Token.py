from enum import Enum, auto

class TokenType(Enum):
    
    IDINT     = auto()
    IDFLOAT   = auto()
    IDINTEGER = auto()
    IDSTRING  = auto()
    IDBOOL    = auto()

    FLOAT = auto()
    INTEGER = auto()
    STRING = auto()
    BOOL = auto()

    IDENTIFIER = auto()
    


    EQUAL = auto()  #=
    EQUAL_EQUAL = auto()  #==
    BANG_EQUAL = auto()  #!=
    BANG = auto()  #!
    LESS = auto()  #<
    LESS_EQUAL = auto()  #<=
    
    GREATER = auto()  #>
    GREATER_EQUAL = auto () #>=

    LPAREN = auto()#(
    RPAREN = auto()#)
    LBRACE = auto()#{
    RBRACE = auto()#}
    LBRACKET = auto()#[
    RBRACKET = auto()#]
    COLON = auto()#:
    DOT = auto()#.

    BREAK = auto()
    CONTINUE = auto()
    GOTO = auto()
        
    
    
    MOD = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    XOR = auto()
    POW = auto()

    PLUS = auto()#+
    MINUS = auto()#-
    STAR = auto()#*
    SLASH = auto()#/
    PERCENT = auto()#%
    CARET = auto()#^
    SEMICOLON = auto()#;
    
    NIL = auto()
    TRUE = auto()
    FALSE = auto()

    
    ELSE = auto()
    IF = auto()
    ELSEIF = auto()
    WHILE = auto()
    DO = auto() 
    RETURN = auto()
    COMMA = auto()
    
    PRINT = auto()
    FUNCTION = auto()
    PROCESS = auto()
    STRUCT = auto()
    

    EOF = auto()


class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        if self.literal is None:
            return f"{self.type} {self.lexeme}"
        else:
            return f"{self.type}  {self.literal}"
    

