
class Node:
    def accept(self, visitor):
        pass

class Empty(Node):
    def __init__(self):
        pass

    def accept(self, visitor):
        print("Empty")
        return "None"

class Binary(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Unary(Node):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)
    
class Logical(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

class Literal(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Grouping(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Variable(Node):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)


class Assign(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


# ****************************************************Statements



class ExpressionStmt(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class PrintStmt(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)




class EvalStmt(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_eval_stmt(self)
    
class IfStmt(Node):
    def __init__(self, condition, then_branch, elif_branches, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches  # Lista de ElifStmt
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class ElifStmt(Node):
    def __init__(self, condition, then_branch):
        self.condition = condition
        self.then_branch = then_branch

    def accept(self, visitor):
        return visitor.visit_elif_stmt(self)    
    
class WhileStmt(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.is_break=False
        self.is_continue = False
        self.depth = 0
        self.first_time = True

    def accept(self, visitor):
        visitor.last_loop =  self
        return visitor.visit_while_stmt(self)

class DoWhileStmt(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.is_break=False
        self.is_continue = False
        self.depth = 0

    def accept(self, visitor):
        return visitor.visit_do_while_stmt(self)
    
class LoopStmt(Node):
    def __init__(self, body):
        self.body = body
        self.is_break    = False
        self.is_continue = False
        self.depth = 0
        

    def accept(self, visitor):
        return visitor.visit_loop_stmt(self)

class SwitchStmt(Node):
    def __init__(self, expression, cases, default_case=None):
        self.expression = expression
        self.cases = cases  
        self.default_case = default_case

    def accept(self, visitor):
        return visitor.visit_switch_stmt(self)

class CaseStmt(Node):
    def __init__(self, value, body):
        self.value = value
        self.body = body

    def accept(self, visitor):
        return visitor.visit_case_stmt(self)

class BreakStmt(Node):
    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit_break_stmt(self)
    





class ContinueStmt(Node):
    def __init__(self):
        pass


    def accept(self, visitor):
        return visitor.visit_continue_stmt(self)    
    

class ReturnStmt(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)



class BlockStmt(Node):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class VarDecl(Node):
    def __init__(self, type, name, initializer):
        self.type = type
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_decl_stmt(self)

class Program(Node):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def accept(self, visitor):
        return visitor.visit_program_stmt(self)


#processos
class ProcessStmt(Node):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body




    def accept(self, visitor):
        return visitor.visit_process_stmt(self)

class Parameter(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def accept(self, visitor):
        return visitor.visit_parameter(self)

class FrameStmt(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_frame_stmt(self)
    

class StartProcessStmt(Node):
    def __init__(self, process_name, arguments):
        self.process_name = process_name
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_start_process_stmt(self)    