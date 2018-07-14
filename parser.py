# Grammar 
# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
# addition       → _multiplication ( ( "-" | "+" ) _multiplication )* ;
# _multiplication → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#              | primary ;
# primary        → NUMBER | STRING | "false" | "true" | "nil"
#               | "(" expression ")" ;

from expr import * 
from tokens import TokenType 

class Parser:
	class ParseError(Exception):
		pass 

	def __init__(tokens):
		self.tokens = tokens 
		self.current = 0

	def parse(self):
		try:
			return self._expression()
		except ParseError as e:
			return None # will sync here.
	
	def _expression(self):
		self._equality()

	def _equality(self):
		expr = self._comparison()
		while (self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
			operator = self._previous()
			right = self._comparison()
			expr = Binary(expr, operator, right)

		return expr 

	def _comparison(self):
		expr = self._addition()
		while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
			operator = self._previous()
			right = addition()
			expr = Binary(expr, operator, right)

		return expr 

	def _addition(self):
		expr = self._multiplication()
		while self._match(TokenType.MINUS, TokenType.TokenType.PLUS):
			operator = self._previous()
			right = self._multiplication()
			expr = Binary(expr, operator, right)

		return expr 

	def _multiplication(self):
		expr = self._unary()
		while self._match(TokenType.SLASH, TokenType.STAR):
			operator = self._previous()
			right = self._unary()
			expr = Binary(expr, operator, right)

		return expr 

	def unary(self):
		if self._match(TokenType.BANG, TokenType.MINUS):
			operator = self.previous()
			operand = self._unary()
			return Unary(operator, operand)

		return self.primary()

	def primary(self):
		if self._match(TokenType.FALSE):
			return Literal(False)
		elif self._match(True):
			return Literal(True)
		elif self._match(None):
			return Literal(None)
		elif self._match(TokenType.NUMBER, TokenType.STRING):
			return Literal(previous().literal)
		elif self._match(TokenType.LEFT_PAREN):
			expr = self._expression()
			consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
			return Grouping(expr)

		return error(peek(), 'Expect expression')
	def consume(self, token_type, message):
		if self.check(token_type):
			return self.advance()

		return self._error(peek(), message)

	def match(self, *token_types):
		for token_type in token_types:
			if self._check(token_type):
				self._advance()
				return True 

		return False 

	def check(self, token_type):
		if self._is_at_end():
			return False 

		return self._peek().type == token_type

	def _advance(self):
		if not self._is_at_end():
			self.current += 1

		return self._previous()

	def _is_at_end(self):
		return self.peek().type == TokenType.EOF

	def _peek(self):
		return self.tokens[current]

	def _previous(self):
		return self.tokens[current - 1]

	def _error(self, token, msg):
		from lox import error as lox_error
		lox_error(token, msg)
		return ParseError()

	def synchronize(self):
		self._advance()
		STATEMENT_STARTERS = [
			'CLASS',
			'FUN',
			'VAR',
			'FOR',
			'IF',
			'WHILE',
			'PRINT',
			'RETURN',
		]
		while not self._is_at_end():
			if self._previous().type == TokenType.SEMICOLON:
				return 

			if self._peek().type in STATEMENT_STARTERS:
				return  
			
			self._advance()

