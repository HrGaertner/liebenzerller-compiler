

class Code():
	def generateCode(self, env):
		return NotImplemented
	def __repr__(self):
		return "no str() available"

class Program(Code):
	def __init__(self, statements):
		self.statements = statements
	def __repr__(self):
		return "Program(\n"+",\n".join([repr(s) for s in self.statements]) + ")"

class Decl(Code):
	def __init__(self, varname):
		self.varname = varname
	def __repr__(self):
		return "Decl("+repr(self.varname)+")"

class Assign(Code):
	def __init__(self, varname, exp):
		self.varname = varname
		self.exp = exp
	def __repr__(self):
		return repr(self.exp)+" -> "+repr(self.varname)+")"

class Input(Code):
	def __init__(self, varname):
		self.varname = varname
	def __repr__(self):
		return "Input -> " + repr(self.varname)

class Print(Code):
	def __init__(self, exp):
		self.exp = exp
	def __repr__(self):
		return "Print("+repr(self.exp)+")"

class If(Code):
	def __init__(self, exp1, exp2, statements):
		self.exp1 = exp1
		self.exp2 = exp2
		self.statements = statements
	def __repr__(self):
		return f"If({self.exp1}, {self.exp2}) (\n" + \
		"\n".join([repr(s) for s in self.statements]) + ")"

class While(Code):
	def __init__(self, exp1, exp2, statements):
		self.exp1 = exp1
		self.exp2 = exp2
		self.statements = statements
	def __repr__(self):
		return f"While({self.exp1}, {self.exp2}) (\n" + \
		"\n".join([repr(s) for s in self.statements].join("\n") + ")"

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




