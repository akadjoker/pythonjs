

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