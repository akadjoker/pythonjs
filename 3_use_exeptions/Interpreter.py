import time
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser
from Visitor import Visitor
from Ast import  Literal



class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Frame:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        print(f"Undefined variable '{name.lexeme}'.")
        exit(1)


    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        print(f"Undefined variable '{name.lexeme}'.")
        exit(1)


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        # if name in self.values:
        #     print(f"Variable '{name}' already defined.")
        #     exit(1)
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        print(f"Undefined variable '{name.lexeme}'.")
        exit(1)

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        print(f"Undefined variable '{name.lexeme}'.")
        exit(1)

class Interpreter(Visitor):
    def __init__(self):
        self.environment = Environment()

    def interpret(self, program):
        for statement in program.body:
            self.execute(statement)

    def execute(self, stmt):
        return stmt.accept(self)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(value)

    def visit_eval_stmt(self, stmt):
        value = str(self.evaluate(stmt.expression))
        python_expression = value.replace('^', '**')
        print(eval(python_expression))
        return value

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_var_decl_stmt(self, stmt):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_if_stmt(self, stmt):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        else:
            for elif_stmt in stmt.elif_branches:
                if self.evaluate(elif_stmt.condition):
                    self.execute(elif_stmt.then_branch)
                    return
            if stmt.else_branch:
                self.execute(stmt.else_branch)
    
    def visit_elif_stmt(self, expr):
        pass

    def visit_do_while_stmt(self, do_stmt):
        try:
            while True:
                try:
                    for stmt in do_stmt.body:
                        self.execute(stmt)
                except ContinueException:
                    continue
                if not self.evaluate(do_stmt.condition):
                    break
        except BreakException:
            pass
    
    def visit_while_stmt(self, stmt):
        try:
            while self.evaluate(stmt.condition):
                try:
                    self.execute(stmt.body)
                except ContinueException:
                    continue
        except BreakException:
            pass
            
    def visit_for_stmt(self, for_stmt):
            try:
                if for_stmt.initializer is not None:
                    self.execute(for_stmt.initializer)
                while True:
                    if for_stmt.condition is not None and not self.evaluate(for_stmt.condition):
                        break
                    try:
                        self.execute(for_stmt.body)
                    except ContinueException:
                        pass
                    finally:
                        if for_stmt.increment is not None:
                            self.evaluate(for_stmt.increment)
            except BreakException:
                pass

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if left:
                return left
        else:
            if not left:
                return left
        return self.evaluate(expr.right)

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
        elif expr.operator.type == TokenType.PERCENT:
            return left % right
        elif expr.operator.type == TokenType.POWER:
            return left ** right
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

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not right

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_switch_stmt(self, switch_stmt):
        switch_value = self.evaluate(switch_stmt.expression)
        for case in switch_stmt.cases:
            if self.evaluate(case.value) == switch_value:
                for stmt in case.body:
                    self.execute(stmt)
                return  # Exit after the first matching case
        if switch_stmt.default_case:
            for stmt in switch_stmt.default_case:
                self.execute(stmt)

    def visit_case_stmt(self, case_stmt):
        #  não é necessário,  lidamos com `case_stmt` no `visit_switch_stmt`
        pass

    def visit_break_stmt(self, break_stmt):
        raise BreakException()
        

    def visit_continue_stmt(self, continue_stmt):
        raise ContinueException()
    
    def visit_return_stmt(self, return_stmt):
        value = None
        if return_stmt.value is not None:
            value = self.evaluate(return_stmt.value)
        raise ReturnException(value)

    def evaluate(self, expr):
        return expr.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous