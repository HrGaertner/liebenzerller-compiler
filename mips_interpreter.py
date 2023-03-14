from sys import argv

def load_program(file) -> tuple:
    data = list[str]
    jump_points = dict[str:int]

    with open(argv[1], encoding="UTF-8") as file:
        CURRENT_LINE = 0
        IN_PROGRAM = False
        for line in file:
            line = line[:-1]  # Removing newline character
            if line == ".text":
                IN_PROGRAM = True  # Finished (last blank line)
            elif not IN_PROGRAM:
                continue
            elif line.endswith(":"):
                jump_points[data[:-1]] = CURRENT_LINE
            else:
                data.append(line)
                CURRENT_LINE += 1
    
    return data, jump_points


def execute_program(data: list, jump_points: dict) -> None:
    stack = [0]
    variables = dict[str:int]
    regs = {"$sp": 0, "$v0":0}

    def regs_to_num(num: str, regs) -> int:
        if not num.lstrip("-").isdecimal():
            return int(regs[num])
            return int(num)


    CURRENT_LINE = 0
    while CURRENT_LINE < len(data):
        line = data[CURRENT_LINE].replace(",", "").split(" ")
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
                    OFFSET = int(var.split("(")[0]) / 4
                    stack[regs["$sp"] - 4] = regs[reg]
                variables[var] = regs[reg]

            case "lw", reg, var:
                if "$sp" in var:
                    if not var.startswith("("):
                        OFFSET = int(var.split("(")[0]) / 4
                    else:
                        OFFSET = 0
                    regs[reg] = stack[regs["$sp"] + OFFSET]
                else:
                    regs[reg] = variables[var]

            case ["syscall"]:
                if regs["$v0"] == 1:
                    print(regs["$a0"])
                elif regs["$v0"] == 5:
                    regs["$v0"] = input()

            case "bgt", num1, num2, label:
                num1 = regs_to_num(num1)
                num2 = regs_to_num(num2)
                if num1 > num2:
                    CURRENT_LINE = jump_points[label]

            case "j", label:
                CURRENT_LINE = jump_points[label]

            case _:
                raise ValueError("unkown instruction encountered: " + " ".join(line))

        CURRENT_LINE += 1

if __name__ == "__main__":
    with open(argv[1], encoding="UTF-8") as file:
        execute_program(*load_program(file))
