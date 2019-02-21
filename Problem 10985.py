def permute(no, symbols, start=""):
    permutations = []
    if no == 0:
        return [start]
    for i in symbols:
        permutations += permute(no - 1, symbols, start + i)
    return permutations


def combinate(pools, symbols, start=""):
    combinations = []
    if sum(pools) == 0:
        return [start]
    for i, n in enumerate(pools):
        if n != 0:
            combinations += combinate(pools[:i] + [pools[i] - 1] + pools[i + 1:], symbols, start + symbols[i])
    return combinations


numbers = [i for i in range(1, 8)]
numbers.reverse()
operationsets = permute(8, [[i] for i in "+-x/a"], [])
splices = combinate([7, 8], [[0], [1]], [])
print(len(operationsets), "OPERATIONSETS ;", len(splices), "ROUNDS")

for i, splice in enumerate(splices):
    print("ROUND", i + 1)
    for operations in operationsets:
        stack = [9, 8]
        nownumbers = numbers.copy()
        nowoperations = operations.copy()
        for j in splice:
            thing = [nownumbers, nowoperations][j].pop(0)
            try:
                if thing == "+":
                    stack.append(float(stack.pop(-1) + stack.pop(-1)))
                elif thing == "-":
                    stack.append(float(stack.pop(-2) - stack.pop(-1)))
                elif thing == "x":
                    stack.append(float(stack.pop(-1) * stack.pop(-1)))
                elif thing == "/":
                    stack.append(float(stack.pop(-2) / stack.pop(-1)))
                elif thing == "a":
                    a = stack.pop(-2)
                    b = stack.pop(-1)
                    if type(a) == int and type(b) == int:
                        stack.append(int(str(a) + str(b)))
                    else:
                        stack = ["NOPE1"]
                        break
                else:
                    stack.append(thing)
            except IndexError:
                stack = ["NOPE2"]
                break
            except ZeroDivisionError:
                stack = ["NOPE3"]
                break
        if stack[0] == 10958:
            print("SUCCESS", splice, operations)
            quit()

# Solution found on Round 537 for ascending 123456789:
# [0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1] ['+', 'a', 'x', 'x', 'x', '/', '/', '+']
# 1 / (2 / ((3 + 4) * 56 * 7 * 8)) + 9 = 10985
# And on Round 168 for descending 987654321
# [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1] ['a', '+', 'x', '+', 'x', '+', 'x', '+']
# 9 + (8 * (7 + (65 * ((4 * (3 + 2)) + 1)))) = 10985
# Do I win?

# ...

# No. No you don't.

# 10985 =/= 10958.

# You idiot.
