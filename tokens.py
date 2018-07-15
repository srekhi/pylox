class Token:
	def __init__(self, type, lexeme, literal, line):
		self.type = type
		self.lexeme = lexeme
		self.literal = literal
		self.line = line 

	def __str__(self):
		# need to format self.type properly.
		return '%s %s %s' % (self.type, self.lexeme, self.literal)
		
class TokenType:
  # Single-character tokens.
  LEFT_PAREN      = 'LEFT_PAREN'
  RIGHT_PAREN     = 'RIGHT_PAREN'
  LEFT_BRACE      = 'LEFT_BRACE'
  RIGHT_BRACE     = 'RIGHT_BRACE'
  COMMA           = 'COMMA'
  DOT             = 'DOT'
  MINUS           = 'MINUS'
  PLUS            = 'PLUS'
  SEMICOLON       = 'SEMICOLON'
  SLASH           = 'SLASH'
  STAR            = 'STAR'

  # One or two character tokens.
  BANG            = 'BANG'
  BANG_EQUAL      = 'BANG_EQUAL'
  EQUAL           = 'EQUAL'
  EQUAL_EQUAL     = 'EQUAL_EQUAL'
  GREATER         = 'GREATER'
  GREATER_EQUAL   = 'GREATER_EQUAL'
  LESS            = 'LESS'
  LESS_EQUAL      = 'LESS_EQUAL'

  # Literals.
  IDENTIFIER      = 'IDENTIFIER'
  STRING          = 'STRING'
  NUMBER          = 'NUMBER'

  # Keywords.
  AND             = 'AND'
  CLASS           = 'CLASS'
  ELSE            = 'ELSE'
  FALSE           = 'FALSE'
  FUN             = 'FUN'
  FOR             = 'FOR'
  IF              = 'IF'
  NIL             = 'NIL'
  OR              = 'OR'
  PRINT           = 'PRINT'
  RETURN          = 'RETURN'
  SUPER           = 'SUPER'
  THIS            = 'THIS'
  TRUE            = 'TRUE'
  VAR             = 'VAR'
  WHILE           = 'WHILE'

  EOF             = 'EOF'

