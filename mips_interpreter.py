from sys import argv


def load_program(program) -> tuple[list[str], dict[str, int]]:
    data: list[str] = []
    jump_points: dict[str, int] = {}

    with open(argv[1], encoding="UTF-8") as program:
        current_line = 0
        in_program = False
        for line in program:
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

    return data, jump_points


def execute_program(data: list[str], jump_points: dict[str, int]) -> None:
    stack = [0]
    variables: dict[str, int] = {}
    regs = {"$sp": 0, "$v0": 0}

    def regs_to_num(num: str) -> int:
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
                regs[erg] = regs_to_num(num1) * regs_to_num(num2)

            case "add", erg, num1, num2:
                regs[erg] = regs_to_num(num1) + regs_to_num(num2)
                if erg == "$sp":
                    if regs[erg] >= len(stack):
                        stack.append(0)

            case "sw", reg, "($sp)":
                stack[regs["$sp"]] = regs[reg]

            case "sw", reg, var:
                if "$sp" in var:
                    offset = int(var.split("(")[0]) / 4
                    stack[regs["$sp"] - 4] = regs[reg]
                variables[var] = regs[reg]

            case "lw", reg, var:
                if "$sp" in var:
                    if not var.startswith("("):
                        offset = int(var.split("(")[0]) / 4
                    else:
                        offset = 0
                    regs[reg] = stack[regs["$sp"] + offset]
                else:
                    regs[reg] = variables[var]

            case ["syscall"]:
                if regs["$v0"] == 1:
                    print(regs["$a0"])
                elif regs["$v0"] == 5:
                    regs["$v0"] = input()

            case "bgt", num1, num2, label:
                if regs_to_num(num1) > regs_to_num(num2):
                    current_line = jump_points[label]

            case "j", label:
                current_line = jump_points[label]

            case _:
                raise ValueError("unkown instruction encountered: " + " ".join(line))

        current_line += 1


if __name__ == "__main__":
    with open(argv[1], encoding="UTF-8") as file:
        execute_program(*load_program(file))
