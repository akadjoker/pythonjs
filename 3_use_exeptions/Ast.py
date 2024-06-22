
class Expr:
    def accept(self, visitor):
        pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)
    
class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)



# Statements


class Stmt:
    def accept(self, visitor):
        pass

class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class EvalStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_eval_stmt(self)
    
class IfStmt:
    def __init__(self, condition, then_branch, elif_branches, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches  # Lista de ElifStmt
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class ElifStmt:
    def __init__(self, condition, then_branch):
        self.condition = condition
        self.then_branch = then_branch

    def accept(self, visitor):
        return visitor.visit_elif_stmt(self)    
    
class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class DoWhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_do_while_stmt(self)
    
class ForStmt:
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body
    def accept(self, visitor):
        return visitor.visit_for_stmt(self)

class SwitchStmt:
    def __init__(self, expression, cases, default_case=None):
        self.expression = expression
        self.cases = cases  
        self.default_case = default_case

    def accept(self, visitor):
        return visitor.visit_switch_stmt(self)

class CaseStmt:
    def __init__(self, value, body):
        self.value = value
        self.body = body

    def accept(self, visitor):
        return visitor.visit_case_stmt(self)
class BreakStmt:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit_break_stmt(self)

class ContinueStmt:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_continue_stmt(self)    
    

class ReturnStmt:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)



class BlockStmt(Stmt):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class VarDecl(Stmt):
    def __init__(self, type, name, initializer):
        self.type = type
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_decl_stmt(self)

class Program(Stmt):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def accept(self, visitor):
        return visitor.visit_program_stmt(self)
