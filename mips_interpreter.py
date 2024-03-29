from sys import argv


def load_program(program) -> tuple[list[str], dict[str, int]]:
    data: list[str] = []
    jump_points: dict[str, int] = {}

    in_program = False
    for line in program:
        line = line[:-1]  # Removing newline character
        if line == ".text":
            in_program = True  # Finished (last blank line)
            current_line = 0
        elif not in_program:
            continue
        elif line.endswith(":"):
            jump_points[line[:-1]] = current_line
        else:
            data.append(line)
            current_line += 1

    return data, jump_points


def execute_program(data: list[str], jump_points: dict[str, int]) -> None:
    stack = [0, 0]
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
                if erg == "$sp":
                    if abs((regs_to_num(num1) - regs_to_num(num2)) / 4) >= len(stack):
                        stack.append(0)
                    regs[erg] = regs_to_num(num1) - regs_to_num(num2)
                else:
                    regs[erg] = regs_to_num(num1) + regs_to_num(num2)

            case "sw", reg, "($sp)":
                stack[int(regs["$sp"] / 4)] = regs[reg]

            case "sw", reg, var:
                if "$sp" in var:
                    offset = int(var.split("(")[0])
                    stack[int((regs["$sp"] - offset) / 4)] = regs[reg]
                variables[var] = regs[reg]

            case "lw", reg, var:
                if "$sp" in var:
                    if not var.startswith("("):
                        # Always a multiple of 4
                        offset = int(int(var.split("(")[0]) / 4)
                    else:
                        offset = 0
                    regs[reg] = stack[int((regs["$sp"] + offset) / 4)]
                else:
                    regs[reg] = variables[var]

            case ["syscall"]:
                if regs["$v0"] == 1:
                    print(regs["$a0"])
                elif regs["$v0"] == 5:
                    regs["$v0"] = int(input())

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
