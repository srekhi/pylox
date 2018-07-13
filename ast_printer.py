from expr import *
from tokens import *

class AstPrinter(ExprVisitor): # AST Printer implementing Visitor Pattern by extending ExprVisitor.
	def print(self, expr):
		# via visitor pattern, we've added ability to print out 
		# expression objects without needing to add print functionality to the classes
		return expr.accept(self)

	def visitBinaryExpr(self, expr):
		return self._parenthesize(expr.operator.lexeme, expr.left, expr.right);

	def visitGroupingExpr(self, expr):
		return self._parenthesize("group", expr.expression)

	def visitLiteralExpr(self, expr):
		if (expr.value == None): 
			return "nil";
		return str(expr.value)

	def visitUnaryExpr(self, expr):
		return self._parenthesize(expr.operator.lexeme, expr.right)

	def _parenthesize(self, name, *exprs):
		builder = ['(', name]
		for expr in exprs:
			builder.append(' ')
			builder.append(expr.accept(self))

		builder.append(')')

		return ''.join(builder)


if __name__ == '__main__':
	expression = Binary(
		Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)), 
		Token(TokenType.STAR, "*", None, 1), 
		Grouping(Literal(45.67))
	)

	print(AstPrinter().print(expression))