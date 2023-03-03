import sys

stack = [0]
vars = {}
jump_points = {}
regs = {"$sp": 0, "$v0":0}

data = []
with open("test.asm") as file:  # sys.argv[1]
    current_line = 0
    in_program = False
    for line in file:
        line = line[:-1]  # Removing newline character
        if line == ".text":
            in_program = True  # Finished (last blank line)
        elif not in_program:
            continue
        elif line.endswith(":"):
            jump_points[data[:-1]] = current_line
        else:
            data.append(line)
            current_line += 1


def regs_to_num(num):
    if not num.lstrip("-").isdecimal():
        return int(regs[num])
    return int(num)


current_line = 0
while current_line < len(data):
    line = data[current_line].replace(",", "").split(" ")
    match line:
        case "li", reg, num:
            regs[reg] = int(num)
        
        case "mul", erg, num1, num2:
            num1 = regs_to_num(num1)
            num2 = regs_to_num(num2)
            regs[erg] = regs[num1] * regs[num2]
        
        case "add", erg, num1, num2:
            num1 = regs_to_num(num1)
            num2 = regs_to_num(num2)
            if erg == "$sp":
                if num1 + num2 >= len(stack):
                    stack.append(0)
            regs[erg] = num1 + num2
        
        case "sw", reg, "($sp)":
            stack[regs["$sp"]] = regs[reg]
        
        case "sw", reg, var:
            if "$sp" in var:
                offset = int(var.split("(")[0]) / 4
                stack[regs["$sp"] - 4] = regs[reg]
            vars[var] = regs[reg]
        
        case "lw", reg, var:
            if "$sp" in var:
                if not var.startswith("("):
                    offset = int(var.split("(")[0]) / 4
                else:
                    offset = 0
                regs[reg] = stack[regs["$sp"] + offset]
            else:
                regs[reg] = vars[var]
        
        case ["syscall"]:
            if regs["$v0"] == 1:
                print(regs["$a0"])
            elif regs["$v0"] == 5:
                regs["$v0"] = input()
        
        case "bgt", num1, num2, label:
            num1 = regs_to_num(num1)
            num2 = regs_to_num(num2)
            if num1 > num2:
                current_line = jump_points[label]
        
        case "j", label:
            current_line = jump_points[label]

        case _:
            raise Exception("unkown instruction encountered: " + " ".join(line))
    
    current_line += 1