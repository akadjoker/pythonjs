import time
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser
from Visitor import Visitor
from Ast import  *
import threading
import time
import asyncio


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        if name in self.values:
            print(f"Variable '{name}' already defined.")
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name)
        print(f"Undefined variable '{name}'.")
        


    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        print(f"Undefined variable '{name}'.")


class ProcessInstance:
    def __init__(self,  ID,environment, process_stmt):
        self.name = process_stmt.name
        self.process_stmt = process_stmt
        self.variables = Environment(environment)
        self.current_statement = 0
        self.count_steps =len(process_stmt.body)
        self.ID = ID
        self.done = False
        self.add_variable("name", self.name)
        self.add_variable("ID", self.ID)
        self.add_variable("x", 0.0)
        self.add_variable("y", 0.0)
        self.add_variable("scale", 0.0)
        self.add_variable("graph", 0)

    def add_variable(self, name, value):
        self.variables.define(name, value)
    
    def get_variable(self, name):
        return self.variables.get(name)
        
    def set_variable(self, name, value):
        self.variables.assign(name, value)


    def run(self, interpreter):
        self.done = False
        self.current_statement = 0
        interpreter.execute_block(self.process_stmt.body, self.variables)

    async def step(self, interpreter):
        if self.done:
            return False
        if self.count_steps==0:
            self.done = True
            return False
        
        if self.current_statement < self.count_steps:
            statement = self.process_stmt.body[self.current_statement]
            state = interpreter.execute_process_statement(statement, self.variables)
            self.current_statement += 1            
            if state:
                print("Frame")
                return True  # Indica que a execução deve pausar para a próxima iteração
        #print(self.count_steps," ", self.current_statement)
        if self.current_statement >= self.count_steps: 
            self.done = True
        return False


def main_run(vm):
    done = False
    while not done: 
        if len(vm.active_processes) == 0:
            break
        #print(len(vm.active_processes)," ", vm.active_processes[0].name)
        for process_instance in vm.active_processes:
            if process_instance.done:
                vm.active_processes.remove(process_instance)
                continue
            if process_instance.step(vm):
                break
 
    print("All processes finished.")
class Interpreter(Visitor):
    def __init__(self):
        self.environment = Environment()
        self.last_loop = None
        self.depth = 0 # loops depth
        self.processes = {}
        self.process_names = {}
        self.active_processes = []
        self.ProcessID = 10000
        self.active_threads = []
        self.loop = False
        self.statements = []
        self.program = None



    async def interpret(self, program):
        for statement in program.body:
            await self.execute(statement)
        # while self.active_processes:
        #     next_processes = []
        #     for process_instance in self.active_processes:
        #         if process_instance.step(self):
        #             next_processes.append(process_instance)
        #     self.active_processes = next_processes

    async def run(self, stmts):
        count = len(stmts)
        await self.execute_block(stmts, self.environment)
        for i in range(1,count):
            await self.execute(stmts[i])
        program = stmts[0]
        await self.execute_block(program.body, self.environment)
        #for statement in program.body:
        #    self.execute(statement)
        #thread = threading.Thread(target=main_run, args=(self,))
        #thread.start()
        #thread.join()
      

    async def debug(self):
        print("-------------------------------------------")
        print(" Process: ")
        for process in self.active_processes:
            print("     ",process.name)
            print("         Local variables: ")
            for var in process.variables.values:
                literal = process.get_variable(var)
                print("             ",var," = ",literal)

        print(" Global variables: ")
        for var in self.environment.values:
            print("     ",var)
        print("-------------------------------------------")
        
    async def evaluate(self, expr):
        try:
            return await expr.accept(self)
        except  Exception as X:
            print("Evaluate expression Error: "+str(X)+" : "+str(expr))

    async def execute(self, stmt):
        try:
            return await stmt.accept(self)
        except Exception as e:
            print(f"Execute Error: {e} in node {type(stmt).__name__}")
        

    async def visit_expression_stmt(self, stmt):
        return await self.evaluate(stmt.expression)

    async def visit_print_stmt(self, stmt):
        value = await self.evaluate(stmt.expression)
        print(value)

    async def visit_eval_stmt(self, stmt):
        value = str(await self.evaluate(stmt.expression))
        python_expression = value.replace('^', '**')
        print(eval(python_expression))
        return value

    async def visit_block_stmt(self, stmt):
        return self.execute_block(stmt.statements, Environment(self.environment))

    async def visit_var_decl_stmt(self, stmt):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    

    async def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name.lexeme, value)
        return value

    async def visit_if_stmt(self, stmt):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        else:
            for elif_stmt in stmt.elif_branches:
                if self.evaluate(elif_stmt.condition):
                    self.execute(elif_stmt.then_branch)
                    return
            if stmt.else_branch:
                self.execute(stmt.else_branch)
    
    async def visit_elif_stmt(self, expr):
        pass

    async def visit_return_stmt(self, return_stmt):
        value = None
        if return_stmt.value is not None:
            value = self.evaluate(return_stmt.value)
        return value
        
    async def visit_break_stmt(self, break_stmt):
        if (self.last_loop is not None):
            self.last_loop.is_break = True


    async def visit_continue_stmt(self, continue_stmt):
        if (self.last_loop is not None):
            self.last_loop.is_continue = True

    

    
    async def visit_do_while_stmt(self, do_while_stmt):
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
    
    async def visit_while_stmt(self, while_stmt):# while && for 
        self.depth += 1
        self.last_loop  = while_stmt
        self.last_loop.is_break    = False
        self.last_loop.is_continue = False
        self.depth      = self.depth 
        while True:
            self.last_loop  = while_stmt    
            result =await self.evaluate(while_stmt.condition)
            if not result or while_stmt.is_break:
                break
            await self.execute(while_stmt.body)
        self.last_loop = None
        self.depth -= 1


      

    async def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if left:
                return left
        else:
            if not left:
                return left
        return self.evaluate(expr.right)

    async def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, int) and isinstance(right, int):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, float) and isinstance(right, float):
                return left + right
            elif isinstance(left, int) and isinstance(right, str):
                return str(left) + right
            elif isinstance(left, str) and isinstance(right, int):
                return left + str(right)
            elif isinstance(left, float) and isinstance(right, int):
                return left + float(right)
            elif isinstance(left, int) and isinstance(right, float):
                return float(left) + right
            else:
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

    async def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not right

    async def visit_literal_expr(self, expr):
        return expr.value

    async def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    async def visit_variable_expr(self, expr):
        return self.environment.get(expr.name.lexeme)

    async def visit_switch_stmt(self, switch_stmt):
        switch_value = await self.evaluate(switch_stmt.expression)
        for case in switch_stmt.cases:
            if self.evaluate(case.value) == switch_value:
                for stmt in case.body:
                    await self.execute(stmt)
                return  # Exit after the first matching case
        if switch_stmt.default_case:
            for stmt in switch_stmt.default_case:
                await self.execute(stmt)

    async def visit_case_stmt(self, case_stmt):
        #  não é necessário,  lidamos com `case_stmt` no `visit_switch_stmt`
        pass


    async def visit_process_stmt(self, process_stmt):
        self.processes[process_stmt.name] = process_stmt
        pass

    async def visit_frame_stmt(self, frame_stmt):
        pass  # 'frame' 

    async def visit_start_process_stmt(self, start_process_stmt):
        process_name = start_process_stmt.process_name.lexeme
        args = [await self.evaluate(arg) for arg in start_process_stmt.arguments]
        await self.start_process(process_name, args)

    async def start_process(self, name, args):
        print("Start process "+str(name) + " " + str(args))
        process_stmt = self.processes.get(name)
        if not process_stmt:
            print(f"Undefined process '{name}'.")
            return 

        if len(args) != len(process_stmt.parameters):
            print(f"Expected {len(process_stmt.parameters)} arguments but got {len(args)}.")
            return

        
        self.ProcessID += 1
        process_instance = ProcessInstance(self.ProcessID,self.environment,process_stmt)
        # process_instance.add_variable("name", self.evaluate(Literal(process_instance.name)))
        # process_instance.add_variable("id", self.evaluate(Literal(self.ProcessID)))
        # process_instance.add_variable("x", self.evaluate(Literal(0.0)))
        # process_instance.add_variable("y", self.evaluate(Literal(0.0)))
        # process_instance.add_variable("scale", self.evaluate(Literal(0.0)))
        # process_instance.add_variable("graph", self.evaluate(Literal(0)))
        


        

        for param, arg in zip(process_stmt.parameters, args):
            literal = Literal(arg)
            process_instance.add_variable(param.name.lexeme, self.evaluate(literal))

        # thread = threading.Thread(target=process_instance.run, args=(self,))
        # thread.start()
        # self.active_threads.append(thread)
        
        self.active_processes.append(process_instance)            

        #self.execute_block(process_stmt.body, process_instance.variables)

    async def execute_process_statement(self, statement, environment):
        previous = self.environment
        try:
            self.environment = environment
            if self.last_loop is not None:
                self.last_loop.is_break    = False
                self.last_loop.is_continue = False
            process = True
            if self.last_loop and self.last_loop.is_break:
                process = False
            if self.last_loop and self.last_loop.is_continue:
                process = False 
                return False

            if process:    
                await self.execute(statement)

            if self.last_loop and self.last_loop.is_break:
                return
            if isinstance(statement, FrameStmt):
                        frame_value = self.evaluate(statement.value)
                        sleep_time = (100 - frame_value) / 100.0
                        if frame_value < 100:
                            #print("Frame:",sleep_time)
                            time.sleep(sleep_time)
                        return True

        except Exception as e:
            print(f"Block Error: {e}")
        finally:
            self.environment = previous

    async def execute_block(self, statements, environment):
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
                    return False
                if isinstance(statement, FrameStmt):
                            frame_value = self.evaluate(statement.value)
                            sleep_time = (100 - frame_value) / 100.0
                            if frame_value < 100:
                                #print("Frame:",sleep_time)
                                time.sleep(sleep_time)
                            return True
                if process:    
                   await self.execute(statement)

                if self.last_loop and self.last_loop.is_break:
                    break

                                

        except Exception as e:
            print(f"Block Error: {e}")
        finally:
            self.environment = previous