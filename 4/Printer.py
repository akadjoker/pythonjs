from Visitor import Visitor
import time

class ASTPrinter(Visitor):
    def print(self, stmts):
        for statement in stmts:
            print(statement.accept(self))

    def visit_binary_expr(self, expr):
        return f"({self._parenthesize(expr.left)} {expr.operator.lexeme} {self._parenthesize(expr.right)})"

    def visit_unary_expr(self, expr):
        return f"({expr.operator.lexeme} {self._parenthesize(expr.right)})"

    def visit_literal_expr(self, expr):
        return str(expr.value)

    def visit_grouping_expr(self, expr):
        return f"(group {self._parenthesize(expr.expression)})"

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def visit_assign_expr(self, expr):
        return f"({expr.name.lexeme} = {self._parenthesize(expr.value)})\n"

    def visit_expression_stmt(self, stmt):
        return self._parenthesize(stmt.expression)

    def visit_print_stmt(self, stmt):
        return f"(print [{self._parenthesize(stmt.expression)}])"

    def visit_eval_stmt(self, stmt):
        return f"(val [{self._parenthesize(stmt.expression)}])"
    
    def visit_if_stmt(self, stmt):
        if stmt.else_branch:
            return f"(if {self._parenthesize(stmt.condition)} {self._parenthesize(stmt.then_branch)} else {self._parenthesize(stmt.else_branch)})"
        return f"(if {self._parenthesize(stmt.condition)} {self._parenthesize(stmt.then_branch)})"
    
    def visit_do_while_stmt(self, stmt):
        return f"(do while )"

    def visit_elif_stmt(self, expr):
        return f"(elif )"

    def visit_while_stmt(self, stmt):
        return f"(while {self._parenthesize(stmt.condition)} {self._parenthesize(stmt.body)})"
    
    def visit_logical_expr(self, expr):
        return f"({self._parenthesize(expr.left)} {expr.operator.lexeme} {self._parenthesize(expr.right)})"

    def visit_block_stmt(self, stmt):
        statements = " ".join(self._parenthesize(statement) for statement in stmt.statements)
        return f"\n(block {statements})"

    def visit_var_decl_stmt(self, stmt):
        initializer = self._parenthesize(stmt.initializer) if stmt.initializer else "None"
        return f"({stmt.type.lexeme} {stmt.name.lexeme} = {initializer})\n"
    
    def visit_switch_stmt(self, switch_stmt):
        return f"(switch)"
    
    def visit_case_stmt(self, case_stmt):
        return f"   (case)\n"
    
    def visit_default_stmt(self, default_stmt):
        return f"   (default)\n"
    
    def visit_break_stmt(self, break_stmt):
        return f"(break)\n"
    
    def visit_continue_stmt(self, continue_stmt):
        return f"(continue)\n"

    def visit_return_stmt(self, return_stmt):
        return f"(return )"
    
    def visit_for_stmt(self, for_stmt):
        return f"(for )"

    def visit_program_stmt(self, stmt):
        body = " ".join(self._parenthesize(statement) for statement in stmt.body)
        return f"program ({stmt.name.lexeme})\n {body}"
    def visit_loop_stmt(self, loop_stmt):
        return f"loop \n "
    def visit_process_stmt(self, process_stmt):
        return f"process {process_stmt.name}\n "
    def visit_frame_stmt(self, frame_stmt):
        return f"frame \n "
    def visit_start_process_stmt(self, start_process_stmt):
        return f"start process \n "
    def _parenthesize(self, expr):
        if expr is None:
            return ""
        return expr.accept(self)


