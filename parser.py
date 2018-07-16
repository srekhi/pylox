# Grammar 
# program 		 → statement* EOF;
# declaration    → varDecl | statement ;
# varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
# statement 	 → exprStmt | printStmt
# exprStmt       → expression ";"
# printStmt      → "print" expression ";"
# expression     → equality;
# equality       → comparison ( ( "!=" | "==" ) comparison )*;
# comparison     → addition ( ( ">" | ">=" | "<" | "<=" ) addition )*;
# addition       → _multiplication ( ( "-" | "+" ) _multiplication )*;
# _multiplication → unary ( ( "/" | "*" ) unary )*;
# unary          → ( "!" | "-" ) unary
#              | primary;
# primary        → NUMBER | STRING | IDENTIFIER | "false" | "true" | "nil"
#               | "(" expression ")";
# identifier

# identifier = name of variable being accessed.

from expr import * 
from stmt import * 
from tokens import TokenType 

class Parser:
	class ParseError(Exception):
		pass 

	def __init__(self, tokens):
		self.tokens = tokens 
		self.current = 0
		self.errors = []

	def parse(self):
		statements = []
		while not self._is_at_end():
			statements.append(self._declaration())

		return statements

	def var_declaration(self):
		name = self.consume(TokenType.IDENTIFIER, 'Expect variable name')

		initializer = None 
		if self._match(TokenType.EQUAL):
			initializer = self.expression()

		self._consume(TokenType.SEMICOLON, "Expect ; after variable declaration")
		return new Var(name, initializer)

	def statement(self):
		if self._match(TokenType.PRINT):
			return self._printStatement()

		return self._expressionStatement()

	def _declaration(self):
		try:
			if match(VAR):
				return self.varDeclaration()
		except ParseError:
			self.synchronize()

	def _printStatement(self):
		value = self._expression()
	    consume(SEMICOLON, "Expect ';' after value.");
	    return Print(value);

	def _expressionStatement(self):
		expr = self._expression()

	def _expression(self):
		return self._equality()

	def _equality(self):
		expr = self._comparison()
		while (self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
			operator = self._previous()
			right = self._comparison()
			expr = Binary(expr, operator, right)

		# 3 == (3==5) == 2
		return expr 

	def _comparison(self):
		expr = self._addition()
		while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
			operator = self._previous()
			right = self._addition()
			expr = Binary(expr, operator, right)

		return expr 

	def _addition(self):
		expr = self._multiplication()
		while self._match(TokenType.MINUS, TokenType.PLUS):
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

	def _unary(self):
		if self._match(TokenType.BANG, TokenType.MINUS):
			operator = self._previous()
			operand = self._unary()
			return Unary(operator, operand)

		return self._primary()

	def _primary(self):
		if self._match(TokenType.FALSE):
			return Literal(False)
		elif self._match(TokenType.TRUE):
			return Literal(True)
		elif self._match(TokenType.NIL):
			return Literal(None)
		elif self._match(TokenType.NUMBER, TokenType.STRING):
			return Literal(self._previous().literal)
		elif self._match(TokenType.LEFT_PAREN):
			expr = self._expression()
			self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
			return Grouping(expr)
		elif self._match(TokenType.IDENTIFIER):
			return Variable(self._previous())
		return self._error(self._peek(), 'Expect expression')

	def _consume(self, token_type, message):
		if self._check(token_type):
			return self._advance()

		return self._error(self._peek(), message)

	def _match(self, *token_types):
		for token_type in token_types:
			if self._check(token_type):
				self._advance()
				return True 

		return False 

	def _check(self, token_type):
		if self._is_at_end():
			return False 

		return self._peek().type == token_type

	def _advance(self):
		if not self._is_at_end():
			self.current += 1

		return self._previous()

	def _is_at_end(self):
		return self._peek().type == TokenType.EOF

	def _peek(self):
		return self.tokens[self.current]

	def _previous(self):
		return self.tokens[self.current - 1]

	def _error(self, token, msg):
		from lox import error as lox_error
		lox_error(token, msg)
		self.errors.append(msg)
		return Parser.ParseError()

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

