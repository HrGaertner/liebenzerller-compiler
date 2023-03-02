# TODO: Note variables in the LSN may not start with $ (check)
import logging

logger = logging.getLogger(__name__)


class Environment():
	def __init__(self):
		self.vars = set()
		self.while_count = 0
		self.if_count = 0
    

class Code:
    def generateCode(self, env: Environment):
        return NotImplemented

    def check_var_existence(self, env: Environment, name: str):
        if not name in env.vars:
            logger.error("Variable " + name + " not defined.")
            exit(1)

    def __repr__(self) -> str:
        return "no str() available"


class Block(Code):
    def __init__(self, statements: list):
        self.statements = statements

    def parseDecl(self, env: Environment):
        for s in self.statements:
            if type(s) == Decl:
                env.vars.add(s.varname)
            elif type(s) == Block:
                s.parseDecl(e)

    def generateCode(self, env: Environment) -> str:
		    return "".join([s.generateCode(env) if type(s)!= Decl else "" for s in self.statements])

    def __repr__(self) -> str:
        return ",".join([repr(s) for s in self.statements])


class Program(Block):
    def __init__(self, statements: list):
        super().__init__(statements)

	def generateCode(self, env: Environment) -> str:
        return (
            ".data\n"
            + "\n".join([f"{v}: .word 0" for v in env.vars])
            + super().generateCode(env)
        )


class Decl(Code):
    def __init__(self, varname: str):
        self.varname = varname

    def __repr__(self) -> str:
        return "\nDecl(" + repr(self.varname) + ")"

    def parseDecl(self, env: Environment):
        env.vars.add(self.varname)


class Assign(Code):
    def __init__(self, varname: str, exp: Code):
        self.varname = varname
        self.exp = exp

    def generateCode(self, env: Environment) -> str:
        super().check_var_existence(env, self.varname)
        local_code = "\nlw $t0 ($sp)\nadd $sp, $sp, 4\nsw $t0, " + self.varname
        return local_code

    def __repr__(self) -> str:
        return "\n" + repr(self.exp) + " -> " + repr(self.varname) + ")"


class Input(Code):
    def __init__(self, varname: str):
        self.varname = varname

    def generateCode(self, env: Environment) -> str:
        # TODO instead of varname a expression (making x = 5 +input possible)
        super().check_var_existence(env, self.varname)
        local_code = "\nli $v0, 5\nsw $v0, " + self.varname + "\nsyscall"
        return local_code

    def __repr__(self) -> str:
        return "\nInput -> " + repr(self.varname)


class Print(Code):
    def __init__(self, exp: Code):
        self.exp = exp

    def generateCode(self, env: Environment) -> str:
        mips_exp = self.exp.generateCode(env)
        local_code = "\nli $v0, 1\nlw $a0, ($sp)\nsyscall\nadd $sp, 4"
        return mips_exp + local_code

    def __repr__(self) -> str:
        return "\nPrint(" + repr(self.exp) + ")"


class If(Block):
	  def __init__(self, exp1: Code, exp2: Code, statements: list):
    	  self.exp1 = exp1
		    self.exp2 = exp2
		    super().__init__(statements)
    
	  def generateCode(self, env: Environment) -> str:
		    label = "if" + str(env.if_count)
		    env.if_count += 1
		    start_code = "\n" + self.exp1.generateCode(env) + self.exp2.generateCode(env) + \
					 "\nlw $t0 ($sp)\nlw $t1 4($sp)\nadd $sp, $sp, 8\nbgt $t0, $t1, " + label + "\n"
		    end_code = "\n" + label + ":"
		    return start_code + self.generateBlockCode(env) + end_code

    def __repr__(self) -> str:
        return f"\nIf({self.exp1}, {self.exp2}) (" + super().__repr__() + "\n)"

  
class While(Block):
    def __init__(self, exp1: Code, exp2: Code, statements: list):
        self.exp1 = exp1
        self.exp2 = exp2
        super().__init__(statements)
    
	  def generateCode(self, env: Environment) -> str:
		    label = "while" + str(env.while_count)
		    env.while_count += 1
		    start_code = "\n" + label + "start: \n" + self.exp1.generateCode(env) + self.exp2.generateCode(env) + \
					 "\nlw $t0 ($sp)\nlw $t1 4($sp)\nadd $sp, $sp, 8\nbgt $t0, $t1, " + label
		    end_code = "\nj " + label + "start\n" + label + "end:"
		    return start_code + self.generateBlockCode(env) + end_code
    
	  def __repr__(self) -> str:
		    return f"\nWhile({self.exp1}, {self.exp2}) (" + super().__repr__() + "\n)"


class Sum(Code):
    def __init__(self, exp1: Code, exp2: Code):
        self.exp1 = exp1
        self.exp2 = exp2

    def generateCode(self, env: Environment) -> str:
        mips_exp = self.exp1.generateCode(env)
        mips_exp += self.exp2.generateCode(env)
        local_code = (
            "\nlw $t0, ($sp)\nadd $sp 4\nlw $t1, (sp)\nadd $t2, $t1, $t0\nsw $t2, ($sp)"
        )
        return mips_exp + local_code

    def __repr__(self) -> str:
        return repr(self.exp1) + " + " + repr(self.exp2)


class Product(Code):
    def __init__(self, exp1: Code, exp2: Code):
        self.exp1 = exp1
        self.exp2 = exp2
	
	  def generateCode(self, env: Environment) -> str:
		    mips_exp = self.exp1.generateCode(env)
		    mips_exp += self.exp2.geneateCode(env) 
		    local_code = "lw $t0, ($sp)\nmul $sp 4\nlw $t1, (sp)\nadd $t2, $t1, $t0\nsw $t2, ($sp)"
		    return mips_exp + local_code
	
    def __repr__(self) -> str:
        return repr(self.exp1) + " * " + repr(self.exp2)
        

class Negative(Code):
    def __init__(self, exp: Code):
        self.exp = exp

    def generateCode(self, env: Environment) -> str:
        local_code = "\nlw $t0, ($sp)\nmul $t1, $t0, -1\nsw $t0, ($sp)"
        return local_code

    def __repr__(self) -> str:
        return "-" + repr(self.exp)


class Var(Code):
    def __init__(self, varname: str):
        self.varname = varname
    
    def generateCode(self, env: Environment) -> str:
            super().check_var_existence(env, self.varname)
            local_code = "lw $t0, " + self.varname + "\nadd $sp, -4\nsw $t0, ($sp)"
            return local_code

    def __repr__(self) -> str:
        return self.varname


class Num(Code):
    def __init__(self, number: int):
        self.number = number

    def generateCode(self, env: Environment) -> str:
        local_code = "li $t0, " + str(self.number) + "\nadd $sp -4\nsw $t0 ($sp)"
        return

    def __repr__(self) -> str:
        return repr(self.number)


# Beispielprogramm
ast = Program(
    [
        Decl("x"),
        Decl("y"),
        Decl("z"),
        Assign("x", Sum(Product(Num(1), Num(2)), Num(3))),
        Input("y"),
        While(
            Num(0),
            Var("x"),
            [
                Assign("x", Sum(Var("x"), Negative(Num(1)))),
                Assign("z", Sum(Var("z"), Var("y"))),
            ],
        ),
        If(Var("z"), Num(1), [Print(Num(0))]),
        If(Num(0), Var("z"), [Print(Var("z"))]),
    ]
)

print(ast)
e = Environment()
ast.parseDecl(e)
print(ast.generateCode(e))
