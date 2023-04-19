import unittest
from unittest.mock import patch
from io import StringIO
import mips_interpreter as mi
import mips_compiler as mc

def code_to_interpret(code: str):
    return [i+"\n" for i in code.split("\n")][:-1]

@patch('sys.stdout', new_callable = StringIO)
@patch('sys.stderr', new_callable = StringIO)
def execute_program(program: mc.Program, stderr, stdout):
    e = mc.Environment()
    program.parse_decl(e)
    mi.execute_program(*mi.load_program(code_to_interpret(program.generate_code(e))))
    return stdout.getvalue()

class Compiler_Tests(unittest.TestCase):
    def test_print(self):
        program = mc.Program([mc.Print(mc.Num(4))])
        self.assertEqual(execute_program(program), "4\n")

    def test_while(self):
        # BUG not working endless loop
        program = mc.Program([mc.Decl("x"), mc.Assign("x", mc.Num(0)), mc.Print(mc.Var("x")), mc.While(mc.Num(0), mc.Var("x"), [mc.Assign("x", mc.Sum(mc.Var("x"), mc.Num(1)))]), mc.Print(mc.Var("x"))])
        self.assertEqual(execute_program(program), "5\n")
        
    def test_example_program(self):
        program = mc.Program(
            [
                mc.Decl("x"),
                mc.Decl("y"),
                mc.Decl("z"),
                mc.Assign("z", mc.Num(0)),  # Initalize value (BUG we have to think this through)
                mc.Assign("x", mc.Sum(mc.Product(mc.Num(1), mc.Num(2)), mc.Num(3))),
                mc.Input("y"),
                mc.While(
                    mc.Num(0),
                    mc.Var("x"),
                    [
                        mc.Assign("x", mc.Sum(mc.Var("x"), mc.Negative(mc.Num(1)))),
                        mc.Assign("z", mc.Sum(mc.Var("z"), mc.Var("y"))),
                    ],
                ),
                mc.If(mc.Var("z"), mc.Num(1), [mc.Print(mc.Num(0))]),
                mc.If(mc.Num(0), mc.Var("z"), [mc.Print(mc.Var("z"))]),
            ]
        )
        solution = lambda x: 5*x  # Same as the program aboth
        return True # TODO need to handle input and output

if __name__ == "__main__":
    unittest.main()