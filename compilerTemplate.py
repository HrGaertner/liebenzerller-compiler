class Environment():
	def __init__(self):
		self.vars = set()


class Code():
	def generateCode(self, env):
		return repr(self) # NotImplemented
	def __repr__(self):
		return "no str() available"

class Block(Code):
	def __init__(self, statements):
		self.statements = statements
	def parseDecl(self, env):
		for s in self.statements:
			if type(s) == Decl:
				env.vars.add(s.varname)
			elif type(s) == Block:
				s.parseDecl(e)
	def __repr__(self):
		return ",".join([repr(s) if type(s) != Decl else "" for s in self.statements])

class Program(Block):
	def __init__(self, statements):
		super().__init__(statements)
	def generateCode(self, env):
		return ".data\n" + "\n".join([f"{v}: .word 0"for v in env.vars]) + \
		"\n.text" + "".join([s.generateCode(env) for s in self.statements])
	def __repr__(self):
		return "\nProgram("+ super().__repr__() + "\n)"

class Decl(Code):
	def __init__(self, varname):
		self.varname = varname
	def __repr__(self):
		return "\nDecl("+repr(self.varname)+")"
	def parseDecl(self, env):
		env.vars.add(self.varname)

class Assign(Code):
	def __init__(self, varname, exp):
		self.varname = varname
		self.exp = exp
	def __repr__(self):
		return "\n" + repr(self.exp)+" -> "+ repr(self.varname)+")"

class Input(Code):
	def __init__(self, varname):
		self.varname = varname
	def __repr__(self):
		return "\nInput -> " + repr(self.varname)

class Print(Code):
	def __init__(self, exp):
		self.exp = exp
	def __repr__(self):
		return "\nPrint("+repr(self.exp)+")"

class If(Block):
	def __init__(self, exp1, exp2, statements):
		self.exp1 = exp1
		self.exp2 = exp2
		super().__init__(statements)
	def __repr__(self):
		return f"\nIf({self.exp1}, {self.exp2}) (" + super().__repr__() + "\n)"

class While(Block):
	def __init__(self, exp1, exp2, statements):
		self.exp1 = exp1
		self.exp2 = exp2
		super().__init__(statements)
	def __repr__(self):
		return f"\nWhile({self.exp1}, {self.exp2}) (" + super().__repr__() + "\n)"

class Sum(Code):
	def __init__(self, exp1, exp2):
		self.exp1 = exp1
		self.exp2 = exp2
	def __repr__(self):
		return repr(self.exp1) + " + " + repr(self.exp2)

class Product(Code):
	def __init__(self, exp1, exp2):
		self.exp1 = exp1
		self.exp2 = exp2
	def __repr__(self):
		return repr(self.exp1) + " * " + repr(self.exp2)

class Negative(Code):
	def __init__(self, exp):
		self.exp = exp
	def __repr__(self):
		return "-" + repr(self.exp)

class Var(Code):
	def __init__(self, varname):
		self.varname = varname
	def __repr__(self):
		return self.varname

class Num(Code):
	def __init__(self, number):
		self.number = number
	def __repr__(self):
		return repr(self.number)


# Beispielprogramm
ast = Program([
	Decl("x"),
	Decl("y"),
	Decl("z"),
	Assign("x", Sum(Product(Num(1),Num(2)),Num(3))),
	Input("y"),
	While(Num(0), Var("x"), [
		Assign("x", Sum(Var("x"), Negative(Num(1)))),
		Assign("z", Sum(Var("z"), Var("y")))
	]),
	If(Var("z"), Num(1), [
		Print(Num(0))
	]),
	If(Num(0), Var("z"), [
		Print(Var("z"))
	])
])

print(ast)
e = Environment()
ast.parseDecl(e)
print(ast.generateCode(e))
