

class Visitor:
    def visit_binary_expr(self, expr):
        pass

    def visit_unary_expr(self, expr):
        pass

    def visit_literal_expr(self, expr):
        pass

    def visit_grouping_expr(self, expr):
        pass

    def visit_variable_expr(self, expr):
        pass

    def visit_assign_expr(self, expr):
        pass

    def visit_var_decl_expr(self, expr):
        pass

    def visit_expression_stmt(self, stmt):
        pass

    def visit_print_stmt(self, stmt):
        pass

    def visit_eval_expr(self, expr):
        pass

    def visit_block_stmt(self, stmt):
        pass

    def visit_program_stmt(self, stmt):
        pass

    def visit_if_stmt(self, stmt):
        pass

    def visit_elif_stmt(self, expr):
        pass

    def visit_do_while_stmt(self, do_stmt):
        pass

    def visit_while_stmt(self, stmt):
        pass

    def visit_logical_expr(self, expr):
        pass

    def visit_break_stmt(self, break_stmt):
        pass

    def visit_continue_stmt(self, continue_stmt):
        pass

    def visit_return_stmt(self, return_stmt):
        pass

    def visit_for_stmt(self, for_stmt):
        pass