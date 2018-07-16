from abc import ABC, abstractmethod

class Stmt(ABC): pass

class Expression(Stmt)
	def __init__(expression)
		self.expression = expression

class Print(Stmt)
	def __init__(expression)
		self.expression = expression

class Var(Stmt)
	def __init__(name, initializer)
		self.name = name
		self.initializer = initializer

