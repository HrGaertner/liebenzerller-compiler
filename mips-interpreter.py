import sys

stack = []
vars = {}
regs = {"$sp":0}

in_program = False
with open(sys.args[1]) as file:
    for line in file:
        line = line[:-1] # Removing newline character
        if is_program:
            line = line.replace(" ","").split(",")
            match line:
                case "li", reg, num:
                    regs[reg] = num
                case "mul", erg, num1, num2:
                    if not num1.lstrip("-").isdecimal:
                        num1 = regs[num1]
                    if not num2.lstrip("-").isdecimal:
                        num2 = regs[num2]
                    regs[erg] = regs[num1] * regs[num2]
                case "add", erg, num1, num2:
                    if not num1.lstrip("-").isdecimal:
                        num1 = regs[num1]
                    if not num2.lstrip("-").isdecimal:
                        num2 = regs[num2]
                    if erg == "$sp":
                        if num1+num2>=len(stack):
                            stack.append(0)
                    regs[erg] = num1 + num2
                case "sw", reg, "($sp)":
                    stack["$sp"] = regs[reg]
                case "sw", reg, var:
                    if "$sp" in var:
                        offset = int(var.split("(")[0])/4
                        stack[regs["$sp"]-4] = regs[reg]
                    vars[var] = regs[reg]
                case "lw", reg, var:
                    if "$sp" in var:
                        offset = int(var.split("(")[0])/4
                        regs[reg] = stack[regs["$sp"]-4]
                    regs[reg] = vars[var]
                case "syscall":
                    if regs["$v0"] == 1:
                        print(regs["$a0"])
                    elif regs["$v0"] == 5:
                        regs["$v0"] = input()
                case _:
                    raise Exception("unkown instruction encountered")

        elif line == "main:":
            is_program = True