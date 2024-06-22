import time
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser
from Visitor import Visitor
from Ast import  *


class ProcessInstance:
    def __init__(self, process_stmt, environment):
        self.process_stmt = process_stmt
        self.environment = environment
        self.current_statement = 0

    def step(self, interpreter):
        if self.current_statement < len(self.process_stmt.body):
            statement = self.process_stmt.body[self.current_statement]
            interpreter.execute(statement)
            if isinstance(statement, FrameStmt):
                self.current_statement += 1
                return True  # Indica que a execução deve pausar para a próxima iteração
            self.current_statement += 1
        return False  # Indica que o processo terminou


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


class Interpreter(Visitor):
    def __init__(self):
        self.environment = Environment()
        self.last_loop = None
        self.depth = 0 # loops depth
        self.processes = {}
        self.active_processes = []

    def interpret(self, program):
        for statement in program.body:
            self.execute(statement)
        while self.active_processes:
            next_processes = []
            for process_instance in self.active_processes:
                if process_instance.step(self):
                    next_processes.append(process_instance)
            self.active_processes = next_processes

        
    def evaluate(self, expr):
        try:
            return expr.accept(self)
        except  Exception as X:
            print("Evaluate expression Error: "+str(X)+" : "+str(expr))

    def execute(self, stmt):
        try:
            return stmt.accept(self)
        except Exception as e:
            print(f"Execute Error: {e} in node {type(stmt).__name__}")
        

    def visit_expression_stmt(self, stmt):
        return self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(value)

    def visit_eval_stmt(self, stmt):
        value = str(self.evaluate(stmt.expression))
        python_expression = value.replace('^', '**')
        print(eval(python_expression))
        return value

    def visit_block_stmt(self, stmt):
        return self.execute_block(stmt.statements, Environment(self.environment))

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

    def visit_return_stmt(self, return_stmt):
        value = None
        if return_stmt.value is not None:
            value = self.evaluate(return_stmt.value)
        return value
        
    def visit_break_stmt(self, break_stmt):
        if (self.last_loop is not None):
            self.last_loop.is_break = True


    def visit_continue_stmt(self, continue_stmt):
        if (self.last_loop is not None):
            self.last_loop.is_continue = True

    

    
    def visit_do_while_stmt(self, do_while_stmt):
        self.depth += 1
        self.last_loop  = do_while_stmt
        self.last_loop.is_break    = False
        self.last_loop.is_continue = False
        self.depth      = self.depth
        while True:
            self.last_loop = do_while_stmt
            self.execute(do_while_stmt.body)
            if not self.evaluate(do_while_stmt.condition) or do_while_stmt.is_break:
                break

        self.last_loop = None
        self.depth -= 1
    
    def visit_while_stmt(self, while_stmt):# while && for 
        self.depth += 1
        self.last_loop  = while_stmt
        self.last_loop.is_break    = False
        self.last_loop.is_continue = False
        self.depth      = self.depth 
        while True:
            self.last_loop  = while_stmt    
            result = self.evaluate(while_stmt.condition)
            if not result or while_stmt.is_break:
                break
            self.execute(while_stmt.body)
        self.last_loop = None
        self.depth -= 1


      

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


    def visit_process_stmt(self, process_stmt):
        self.processes[process_stmt.name] = process_stmt
        pass

    def visit_frame_stmt(self, frame_stmt):
        pass  # 'frame' 

            

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            if self.last_loop is not None:
                self.last_loop.is_break    = False
                self.last_loop.is_continue = False
            for statement in statements:
                process = True
                if self.last_loop and self.last_loop.is_break:
                    process = False
                if self.last_loop and self.last_loop.is_continue:
                    process = False 
                    return None

                if process:    
                    self.execute(statement)

                if self.last_loop and self.last_loop.is_break:
                    break


        except Exception as e:
            print(f"Block Error: {e}")
        finally:
            self.environment = previous