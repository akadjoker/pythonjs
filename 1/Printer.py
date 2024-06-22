from Visitor import Visitor


class ASTPrinter(Visitor):
    def print(self, stmt):
        return stmt.accept(self)

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

    def visit_block_stmt(self, stmt):
        statements = " ".join(self._parenthesize(statement) for statement in stmt.statements)
        return f"\n(block {statements})"

    def visit_var_decl_stmt(self, stmt):
        initializer = self._parenthesize(stmt.initializer) if stmt.initializer else "None"
        return f"({stmt.type.lexeme} {stmt.name.lexeme} = {initializer})\n"

    def visit_program_stmt(self, stmt):
        body = " ".join(self._parenthesize(statement) for statement in stmt.body)
        return f"program {stmt.name.lexeme}\n {body}"

    def _parenthesize(self, expr):
        return expr.accept(self)


