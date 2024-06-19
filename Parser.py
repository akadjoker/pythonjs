
from Token import TokenType, Token
from enum import Enum, auto


# program         -> statement* EOF ;
# statement       -> varDecl | exprStmt | block ;
# varDecl         -> "var" IDENTIFIER "=" expression ";" ;
# exprStmt        -> expression ";" ;
# block           -> "begin" statement* "end" ;
# expression      -> term ( ( "+" | "-" ) term )* ;
# term            -> factor ( ( "*" | "/" | "%" ) factor )* ;
# factor          -> primary ( "^" factor )? ;
# primary         -> FLOAT | INTEGER | STRING | IDENTIFIER | "(" expression ")" ;


class Expr:
    pass

    def accept(self, visitor):
        pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    

    def __repr__(self):
        return f'({self.left}, {self.operator}, {self.right})'
    
    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    

    
    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    
    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    
    def __repr__(self):
        return str(self.value)

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class VarDecl(Expr):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
        
    
    
    def accept(self, visitor):
        return visitor.visit_var_decl_expr(self)

class Print(Expr):
    def __init__(self, expression):
        self.expression = expression
    

    
    def accept(self, visitor):
        return visitor.visit_print_expr(self)

class Block(Expr):
    def __init__(self, declarations):
        self.declarations = declarations
    

    
    def accept(self, visitor):
        return visitor.visit_block_expr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

# Name 	       Operators 	    Associates
# Equality   	== !=       	Left
# Comparison 	> >= < <=   	Left
# Term 	        - + 	        Left
# Factor 	    / * 	        Left
# Unary 	    ! - 	        Right

class Ast:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0




    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

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

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise Exception(message)

    def parse(self):
        try:
            statements = []
            while not self.is_at_end():
                statements.append(self.declaration())
            return statements
        except Exception as e:
            print("Error parsing input: " + str(e))
            return None

    def declaration(self):
        if self.match(TokenType.VAR):
            return self.var_declaration()
        else:
            return self.statement()

    def statement(self):
        if self.match(TokenType.BEGIN):
            return self.block()
        elif self.match(TokenType.PRINT):
            return self.print_statement()
        else:
            return self.expression_statement()
    

    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return expr

    def expression(self):
        expr = self.term()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    
    def term(self):
        expr = self.factor()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.CARET):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def print_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'print'.")
        value = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after expression.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        print("ADD GLOBAL VARIAVEL", name.lexeme)
        return VarDecl(name, initializer)
    
    def primary(self):
        if self.match(TokenType.INTEGER):
            return Literal(self.previous().literal)
        elif self.match(TokenType.FLOAT): 
            return Literal(self.previous().literal)
        elif self.match(TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.FALSE):
            return Literal(0)
        elif self.match(TokenType.TRUE):
            return Literal(1)
        elif self.match(TokenType.NIL):
            return Literal(0)
        elif self.match(TokenType.IDENTIFIER):
             return Variable(self.previous())
        elif self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise Exception("Primary Expect expression.",self.peek())

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.varsNames =[]

    
    def print_variables(self):
        print("Variables:", self.variables)

    def addGlobal(self, name, value):
        self.variables[name] = value
        self.varsNames.append(name)
        return len(self.varsNames) - 1

    def getGlobal(self, name):
        return self.variables[name]
    
    def variablesIndex(self, name):
        for i in range(len(self.varsNames)):
            if self.varsNames[i] == name:
                return i
        return -1

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except Exception as e:
            print("Error interpreting input: " + str(e))
            return None
    
    def execute(self, statement):
        print("Accept :",statement)
        statement.accept(self)

    def evaluate(self, exp):
        return exp.accept(self)

    def visit(self, exp):
        if exp is None:
            return None
        return self.evaluate(exp)
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator.type == TokenType.PLUS:
            return left + right
        elif expr.operator.type == TokenType.MINUS:
            return left - right
        elif expr.operator.type == TokenType.STAR:
            return left * right
        elif expr.operator.type == TokenType.SLASH:
            return left / right
        elif expr.operator.type == TokenType.GREATER:
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return left != right
        elif expr.operator.type == TokenType.PERCENT:
            return left % right
        elif expr.operator.type == TokenType.CARET:
            return left ** right
        else :
            raise Exception("Unknown binary operator: " + str(expr.operator.type))
        

    def visit_literal_expr(self, expr):
        return expr.value   
    
    def visit_unary_expr(self, expr):
        right = self.interpret(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not right
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)
    
    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        
    
    def visit_var_decl_expr(self, expr):
        value = self.visit(expr.initializer)
        name  = expr.name.lexeme
        self.addGlobal(name, value)

    def visit_assign_expr(self, expr):
        pass

    def visit_variable_expr(self, expr):
        print("GET VAR")
        pass

    def visit_print_expr(self, expr):
        val = self.visit(expr.expression)
        print("PRINT: ",val)
        return val
        
    