from tokens import Token 
from tokens import TokenType 

class Scanner:
	reserved_words_map = {
	    "and": TokenType.AND,
	    "class": TokenType.CLASS,
	    "else": TokenType.ELSE,
	    "false": TokenType.FALSE,
	    "for": TokenType.FOR,
	    "fun": TokenType.FUN,
	    "if": TokenType.IF,
	    "nil": TokenType.NIL,
	    "or": TokenType.OR,
	    "print": TokenType.PRINT,
	    "return": TokenType.RETURN,
	    "super": TokenType.SUPER,
	    "this": TokenType.THIS,
	    "true": TokenType.TRUE,
	    "var": TokenType.VAR,
	    "while": TokenType.WHILE,
	}
	def __init__(self, source):
		self.source = source # input is string
		self.tokens = []
		self._start = 0
		self._current = 0
		self._line = 1

	def scan_tokens(self):
		while not self.is_at_end():
			self.scan_token()

		self.tokens.append(Token(TokenType.EOF, "", None, self._line))
		return self.tokens 

	def is_at_end(self):
		return self._current >= len(self.source)

	def scan_token(self):
		import lox as Lox 
		char = self._advance()
		if char == '(':
			self._add_token(TokenType.LEFT_PAREN)
		elif char == ')':
			self._add_token(TokenType.RIGHT_PAREN)
		elif char == '{':
			self._add_token(TokenType.LEFT_BRACE)
		elif char == '}':
			self._add_token(TokenType.RIGHT_BRACE)
		elif char == ',':
			self._add_token(TokenType.COMMA)
		elif char == '.':
			self._add_token(TokenType.DOT)
		elif char == '-':
			self._add_token(TokenType.MINUS)
		elif char == '+':
			self._add_token(TokenType.PLUS)
		elif char == ';':
			self._add_token(TokenType.SEMICOLON)
		elif char == '*':
			self._add_token(TokenType.STAR)
		elif char == '!':
			self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
		elif char == '=':
			self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
		elif char == '<':
			self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
		elif char == '>':
			self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
		elif char == '/':
			if self._match('/'): # comment runs until end of line
				while (self._peek() != '\n' and not self.is_at_end()):
					self._advance()
			else:
				self._add_token(TokenType.SLASH)
		elif char == ' ' or char == '\r' or char == '\t':
			return # ignore white space 
		elif char == '\n':
			self._line += 1
		elif char == '"':
			self._handle_string()
		else:
			if self._is_digit(char):
				self._handle_number()
			elif self._is_alpha(char):
				self._handle_identifier()
			else:
				Lox.error(self._line, 'Unexpected character')

	def _handle_identifier(self):
		while (self.is_alpha_numeric(self._peek())):
			self._advance()
	    
		lexeme = self.source[self._start:self._current+1]
		token_type = Scanner.reserved_words_map.get(lexeme, None)
		if (token_type == None):
			token_type = TokenType.IDENTIFIER

		self._add_token(token_type)

	def _is_alpha(self, char):
		return ((char >= 'a' and char <= 'z') or 
		       (char >= 'A' and char <= 'Z') or
		        char == '_')

	def is_alpha_numeric(self, char):
		return self._is_alpha(char) or self._is_digit(char)

	def _is_digit(self, char):
		return char >= '0' and char <= '9'

	def _handle_number(self, char):
		while (self.is_digit(self._peek())):
			self._advance();

		if self._peek() == '.' and self.is_digit(self._peek_next()):
			self._advance()
			while self.is_digit(self._peek()):
				self._advance()

		self._add_token(TokenType.NUMBER, float(source[start:current]))

	def _peek_next(self):
		if self._current + 1 >= len(self.source):
			return '\0'
		return source[current + 1]

	def _handle_string(self):
		import lox as Lox 
		while not self.is_at_end() and self._peek() != '"':
			if self._peek() == '\n':
				self._line += 1
			self._advance()

		if self.is_at_end():
			Lox.error(self._line, 'Unterminated string')
			return 

		# advance past closing '"'
		self._advance()

		# strip surrounding quotes 
		value = source[self._start + 1: self._current]
		self._add_token(TokenType.STRING, value)


	def _advance(self):
		self._current += 1
		return self.source[self._current - 1]

	def _add_token(self, token_type, literal=None):
		lexeme = self.source[self._start: self._current+1]
		self.tokens.append(Token(token_type, lexeme, literal, self._line))

	def _match(self, expected):
		if (self.is_at_end()):
			return False

		if (source[self._current] != expected):
			return False

		self._current += 1
		return True

	def _peek(self):
		if self.is_at_end():
			return '\0'
		if self._current >= len(self.source):
			import pdb; pdb.set_trace()

		return self.source[self._current]
