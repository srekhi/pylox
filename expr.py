from abc import ABC, abstractmethod

# Using visitor pattern, any visitor class can now implement the methods
# and call accept on the relevant object, passing in visitor.

# This follows the open/close principle of OOP; objects are open to extension, closed to modification.
class ExprVisitor(ABC):
	
	@abstractmethod
	def visitBinaryExpr(expr):
		pass 

	@abstractmethod
	def visitGroupingExpr(expr):
		pass

	@abstractmethod
	def visitLiteralExpr(expr):
		pass

	@abstractmethod
	def visitUnaryExpr(expr):
		pass

class Expr(ABC): 
	@abstractmethod
	def accept(visitor):
		pass 

class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visitBinaryExpr(self)

class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitGroupingExpr(self)

class Literal(Expr):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visitLiteralExpr(self)

class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visitUnaryExpr(self)
