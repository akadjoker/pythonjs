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
    PROGRAM = auto()
    


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
    PLUS = auto()#+
    MINUS = auto()#-
    STAR = auto()#*
    SLASH = auto()#/
    PERCENT = auto()#%
    POWER = auto()#^
    SEMICOLON = auto()#;
    COMMA = auto()#,

        
    
    
    MOD = auto()#%
    AND = auto()#&&
    OR = auto()#||
    XOR = auto()#?
 


    
    NIL = auto()
    TRUE = auto()
    FALSE = auto()

    BREAK = auto()
    CONTINUE = auto()
    GOTO = auto()
    SWITCH = auto()
    DEFAULT = auto()
    CASE = auto()
    ELSE = auto()
    IF = auto()
    ELIF = auto()
    WHILE = auto()
    DO = auto() 
    RETURN = auto()
    FOR = auto()
    LOOP = auto()
    
    PRINT = auto()
    EVAL = auto()
    NOW = auto()
    IMPORT = auto()

    FUNCTION = auto()
    PROCEDURE = auto()
    
    PROCESS = auto()
    START = auto()
    FRAME = auto()

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
    

