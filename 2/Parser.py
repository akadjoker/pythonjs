import time
from Token import TokenType, Token
from enum import Enum, auto
from Visitor import Visitor
from Printer import ASTPrinter
from Ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
    
    def consume(self, type, message):   
        if self.check(type):
            return self.advance()
        self.error(self.peek(),message)

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            #if self.previous().type == TokenType.SEMICOLON:
            #    return
            #if self.peek().type in [TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.RETURN]:
            #    return
            self.advance()
    
    def error(self, token, message):
        if token.type == TokenType.EOF:
            print(f"[line {token.line}] Error at end: {message}")
        else:
            print(f"[line {token.line}] Error at '{token.lexeme}': {message}")
        exit(1)
    
    def parse(self):
        return self.program()


    def expression(self):
        return self.assignment()
    
    def assignment(self):
            expr = self.expr_or()
            if self.match(TokenType.EQUAL):# =
                equals = self.previous()
                value = self.assignment()
                if isinstance(expr, Variable):
                    name = expr.name
                    return Assign(name, value)
                self.error(equals, "Invalid assignment target.")

            return expr    

    def expr_or(self):
        expr = self.expr_and()
        if self.match(TokenType.OR):
            operator = self.previous()
            right = self.expr_and()
            return Logical(expr, operator, right)
        return expr
    
    def expr_and(self):
        expr = self.equality()
        if self.match(TokenType.AND):
            operator = self.previous()
            right = self.expr_and()
            return Logical(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):# == !=
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):# > >= < <=
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):# + -
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.power()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator = self.previous()
            right = self.power()
            expr = Binary(expr, operator, right)
        return expr

    def power(self):
        expr = self.unary()
        if self.match(TokenType.POWER):# ^
            operator = self.previous()
            right = self.power()
            expr = Binary(expr, operator, right)
        return expr
    
    def unary(self):
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        
        if self.match(TokenType.TRUE):
            return Literal(True)
        
        if self.match(TokenType.NIL):
            return Literal(None)
        
        if self.match(TokenType.INTEGER):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.FLOAT):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.NOW):
            return Literal(time.time())

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        
        
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Grouping(expr)
        return None
    
    def block(self):
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RBRACE, "Expect '}' after block.")
        return statements

    def declaration(self):
        if self.match(TokenType.IDINT, TokenType.IDFLOAT, TokenType.IDSTRING):
            return self.var_declaration()
        return self.statement()

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()

        if self.match(TokenType.EVAL):
            return self.eval_statement()
        
        if self.match(TokenType.IF):
            return self.if_statement()
        
        if self.match(TokenType.WHILE):
            return self.while_statement()
        
        if self.match(TokenType.DO):
            return self.do_while_statement()
        
        if self.match(TokenType.FOR):
            return self.for_statement()
        
        if self.match(TokenType.LBRACE):
            return BlockStmt(self.block())
        return self.expression_statement()
    
    def print_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'print'.")
        value = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after value.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)
    
    def eval_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'eval'.")
        value = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after value.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return EvalStmt(value)  



    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def program(self):
            self.consume(TokenType.PROGRAM, "Expect 'program' at the beginning.")
            name = self.consume(TokenType.IDENTIFIER, "Expect program name.")
            self.consume(TokenType.SEMICOLON, "Expect ';' after program name.")
            self.consume(TokenType.LBRACE, "Expect '{' to start program body.")
            body = self.block()
            return Program(name, body)

    def var_declaration(self):
        type = self.previous()
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarDecl(type, name, initializer)
    
    def if_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after if condition.")

        then_branch = self.statement()

        elif_branches = []
        while self.match(TokenType.ELIF):
            self.consume(TokenType.LPAREN, "Expect '(' after 'elif'.")
            elif_condition = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after elif condition.")
            elif_then_branch = self.statement()
            elif_branches.append(ElifStmt(elif_condition, elif_then_branch))

        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, elif_branches, else_branch)

    def while_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after while condition.")
        body = self.statement()
        return WhileStmt(condition, body)

    def do_while_statement(self):
        self.consume(TokenType.LBRACE, "Expect '{' to begin do-while body.")
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            body.append(self.statement())
        self.consume(TokenType.RBRACE, "Expect '}' after do-while body.")
        self.consume(TokenType.WHILE, "Expect 'while' after 'do' body.")
        self.consume(TokenType.LPAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after while condition.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after do-while condition.")
        return DoWhileStmt(condition, body)

    def for_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'for'.")
        initializer = None
        if self.match(TokenType.IDINT, TokenType.IDFLOAT):
            initializer = self.var_declaration()
        elif self.match(TokenType.SEMICOLON):
            initializer = None
        else:
            initializer = self.expression_statement()
        
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

       
        increment = None
        if not self.check(TokenType.RPAREN):
            increment = self.expression()

        self.consume(TokenType.RPAREN, "Expect ')' after for clauses.")
        
        body = self.statement()

        if increment is not None:
            body = BlockStmt([body, ExpressionStmt(increment)])
        if condition is None:
            condition = Literal(1)
        body = WhileStmt(condition, body)
        if initializer is not None:
            body = BlockStmt([initializer, body])
        return body
       

        

if __name__ == "__main__":
    tokens = [
        Token(TokenType.PROGRAM, "program", None, 1),
        Token(TokenType.IDENTIFIER, "main", None, 1),
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.LBRACE, "{", None, 2),
        Token(TokenType.IDINT, "int", None, 3),
        Token(TokenType.IDENTIFIER, "a", None, 3),
        Token(TokenType.SEMICOLON, ";", None, 3),
        Token(TokenType.RBRACE, "}", None, 4),
        Token(TokenType.EOF, "", None, 5)
    ]

    parser = Parser(tokens)
    program = parser.parse()
    printer = ASTPrinter()
    print(printer.print(program))
