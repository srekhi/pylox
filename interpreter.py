from expr import ExprVisitor

class Interpreter(ExprVisitor):
	class RuntimeException(Exception):
		def __init__(self, token, message):
			super().__init__(message)
			self.token = token

	def interpret(statements):
		try:
			for statement in statements:
				execute(statement)
		except RuntimeException as error:
			Lox.runtimeError(error)

	def stringify(obj):
		if obj is None:
			return 'nil'
		if type(obj) == float:
			text = str(obj)
			if text[-2:] == '.0':
				text = text[text:-2]
			return text 
		return str(obj)

	def visitLiteralExpr(self, expr):
		return expr.value 

	def visitGroupingExpr(self, expr):
		return evaluate(expr.expression)

	def visitUnaryExpr(self, expr):
		right = evaluate(expr.right)
		op_type = expr.operator.type

		if op_type == TokenType.MINUS:
			checkNumberOperand(expr.operator, right)
			return -1 * float(right)
		elif op_type == TokenType.BANG:
			return not is_truthy(right)

		return None 

	def visitBinaryExpr(self, expr):
		left, right = evaluate(expr.left), evaluate(expr.right)
		op_type = expr.operator.type 
		if op_type == TokenType.MINUS:
	        checkNumberOperands(expr.operator, left, right)
			return float(left) - float(right)
		elif op_type == TokenType.SLASH:
	        checkNumberOperands(expr.operator, left, right)
			return float(left)/float(right)
		elif op_type == TokenType.STAR:
	        checkNumberOperands(expr.operator, left, right)
			return float(left) * float(right)
		elif op_type == TokenType.PLUS:
			if type(left) == float and type(right) == float:
				float(left + right)
			if type(left) == str and type(right) == str:
				return left + right 
			raise RuntimeException(expr.operator, 'Operands must be two nums or two strings')

		elif op_type == TokenType.GREATER:
	        checkNumberOperands(expr.operator, left, right)
			return float(left) > float(right)
		elif op_type == TokenType.GREATER_EQUAL:
	        checkNumberOperands(expr.operator, left, right);
			return float(left) >= float(right)
		elif op_type == TokenType.LESS:
	        checkNumberOperands(expr.operator, left, right);
			return float(left) < float(right)
		elif op_type == TokenType.LESS_EQUAL:
	        checkNumberOperands(expr.operator, left, right);
	        return float(left) <= float(right)
	    elif op_type == TokenType.BANG_EQUAL:
	        checkNumberOperands(expr.operator, left, right);
	    	return not is_equal(left, right)
    	elif op_type == TokenType.EQUAL_EQUAL:
	        checkNumberOperands(expr.operator, left, right);
    		return is_equal(left, right)

		return None 

	def checkNumberOperand(self, operator, operand):
	    if (type(operand) == float):
	    	return

	    raise RuntimeException(operator, 'Operand must be a number')

	def checkNumberOperands(self, operator, left, right):
	    if (type(left) == float and type(right) == float):
	    	return

	    raise RuntimeException(operator, 'Operands must be numbers')


	def is_equal(self, left, right):
	    return left == right

	def is_truthy(self, obj):
		if obj is None:
			return False 
		if type(obj) == bool:
			return bool(obj)

		return True 

	def evaluate(self, expr):
		expr.accept(self)

	def execute(self, stmt):
	    stmt.accept(this);
