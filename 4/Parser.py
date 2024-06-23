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
        self.current_loop = None

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
        # while not self.is_at_end():
        #     if self.previous().type == TokenType.SEMICOLON:
        #         return
        #     if self.peek().type in [TokenType.FUNCTION,TokenType.PROCEDURE,TokenType.STRUCT]:
        #         return
        #     self.advance()
    
    def error(self, token, message):
        if token.type == TokenType.EOF:
            print(f"[line {token.line}] Error at end: {message}")
        else:
            print(f"[line {token.line}] Error at '{token.lexeme}': {message}")
        exit(1)
    
    def parse(self):
        statements = []
        statements.append(self.program())
        while not self.is_at_end():
            statements.append(self.declaration())
        

        #while not self.is_at_end():
        #    statements.append(self.program())
        return statements


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
        
        if self.match(TokenType.LOOP):
            return self.loop_statement()

        if self.match(TokenType.RETURN):
            return self.return_statement()
        
        if self.match(TokenType.CONTINUE):
            return self.continue_statement()
        
        if self.match(TokenType.BREAK):
            return self.break_statement()

        if self.match(TokenType.SWITCH):
            return self.switch_statement()

        if self.match(TokenType.PROCESS):
            return self.process_declaration()

        if self.match(TokenType.START):
            return self.start_process_statement()
        
        if self.match(TokenType.FRAME):
            return self.frame_statement()
        

        
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
        node = WhileStmt(condition, body)
        return node
    
    def do_while_statement(self):
        self.consume(TokenType.LBRACE, "Expect '{' to begin do-while body.")
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            body.append(self.statement())
        #body = self.statement()
        self.consume(TokenType.RBRACE, "Expect '}' after do-while body.")
        self.consume(TokenType.WHILE, "Expect 'while' after 'do' body.")
        self.consume(TokenType.LPAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after while condition.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after do-while condition.")
        return DoWhileStmt(condition, BlockStmt(body))
        
    def loop_statement(self):
        self.consume(TokenType.LBRACE, "Expect '{' to begin loop body.")
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            body.append(self.statement())
        self.consume(TokenType.RBRACE, "Expect '}' after loop body.")
        node = LoopStmt(BlockStmt(body))  
        return node




    def for_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'for'.")

        #1. Initialize
        initializer = None
        if self.match(TokenType.IDINT, TokenType.IDFLOAT):
            initializer = self.var_declaration()
        elif self.match(TokenType.SEMICOLON):
            initializer = None
        else:
            initializer = self.expression_statement()

            
        #2. Condition
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        

        #3. Increment   
        increment = None
        if not self.check(TokenType.RPAREN):
            increment = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after for clauses.")


        #4. Body
  
        
        body = self.statement()

        if increment is not None:
            body = BlockStmt([body, ExpressionStmt(increment)])

        if condition is None:
            condition = Literal(1)

        body = WhileStmt(condition, body)

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

        
       
        

    
    def return_statement(self):
        keyword = self.previous()   
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        return ReturnStmt(keyword, value)


    def break_statement(self):
        node = BreakStmt()
        return node
        

    def continue_statement(self):
        node = ContinueStmt()
        return node
    
    def switch_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'switch'.")
        expression = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after switch expression.")
        self.consume(TokenType.LBRACE, "Expect '{' to begin switch cases.")

        cases = []
        default_case = None

        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.match(TokenType.CASE):
                value = self.expression()
                self.consume(TokenType.COLON, "Expect ':' after case value.")
                self.consume(TokenType.LBRACE, "Expect '{' to begin case body.")
                body = []
                while not self.check(TokenType.RBRACE) and not self.check(TokenType.CASE) and not self.check(TokenType.DEFAULT):
                    body.append(self.statement())
                self.consume(TokenType.RBRACE, "Expect '}' after case body.")
                cases.append(CaseStmt(value, body))
            elif self.match(TokenType.DEFAULT):
                self.consume(TokenType.COLON, "Expect ':' after default.")
                self.consume(TokenType.LBRACE, "Expect '{' to begin default case body.")
                default_case = []
                while not self.check(TokenType.RBRACE) and not self.check(TokenType.CASE):
                    default_case.append(self.statement())
                self.consume(TokenType.RBRACE, "Expect '}' after default case body.")

        self.consume(TokenType.RBRACE, "Expect '}' after switch cases.")
        return SwitchStmt(expression, cases, default_case)


    #Process
    def parameter(self):
        type = None
        if self.match(TokenType.IDINT):
            type = TokenType.IDINT
        elif self.match(TokenType.IDFLOAT):
            type = TokenType.IDFLOAT
        elif self.match(TokenType.IDSTRING):
            type = TokenType.IDSTRING
        elif self.match(TokenType.IDBOOL):
            type = TokenType.IDBOOL
        else:
            print("Error in parameter")
            exit(1)
        name = self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
        return Parameter(type, name)                                      

    
    def process_declaration(self):
        #self.consume(TokenType.PROCESS, "Expect 'process' keyword.")
        name = self.consume(TokenType.IDENTIFIER, "Expect process name.")
        
        self.consume(TokenType.LPAREN, "Expect '(' after process name.")
        
        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters.append(self.parameter())
            while self.match(TokenType.COMMA):
                parameters.append(self.parameter())
        
        self.consume(TokenType.RPAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LBRACE, "Expect '{' before process body.")
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            body.append(self.statement())
        
        self.consume(TokenType.RBRACE, "Expect '}' after process body.")
        
        return ProcessStmt(name.lexeme, parameters, body)
    
    def start_process_statement(self):
        #self.consume(TokenType.START, "Expect 'start' keyword.")
        process_name = self.consume(TokenType.IDENTIFIER, "Expect process name.")
        
        self.consume(TokenType.LPAREN, "Expect '(' after process name.")
        
        arguments = []
        if not self.check(TokenType.RPAREN):
             arguments.append(self.expression())
             while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        self.consume(TokenType.RPAREN, "Expect ')' after arguments.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after process start.")

        print(str(arguments))
        
        return StartProcessStmt(process_name, arguments)

    def frame_statement(self):
        value = None
        if self.match(TokenType.LPAREN): 
            value = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after frame argument.")
        else:
            value = Literal(100)  
        if isinstance(value, Literal) and value.value > 100:
            value = Literal(100)  
        self.consume(TokenType.SEMICOLON, "Expect ';' after 'frame'.")
        return FrameStmt(value)
