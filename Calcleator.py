__author__ = 'Charlie'
# Be aware that calculations are carried out in a human-friendly left-to right way, not stack-friendly,
# though it still takes these items from the end of the stack.
# e.g. 4_5_- >> 4 - 5
#      6_4_choose >> 6C4
#      12_3_** or 12_3_^ >> 12^3
try:
    #qpy:console
    #qpy:2
    import sl4a
    droid = sl4a.Android()
    droidMode = True
except:
    print("Android functionality inactive")
    droidMode = False
import math
ans = 0

while True:
    # having asked for your input
    print("Input reverse Polish expression.")
    # it breaks it up into terms at the _s
    exp = input(">> ").split("_")
    oi = 0
    stack = []
    error = 0
    current = ""
    a = ""
    b = ""
    # then cycles through them and operates accordingly
    try:
        while oi < len(exp):
            current = exp[oi].lower()
            if current == "+":
                # sum of topmost two values
                b = float(stack.pop())
                a = float(stack.pop())
                stack.append(a + b)
            elif current == "-":
                # (penultimate) minus (topmost)
                b = float(stack.pop())
                a = float(stack.pop())
                stack.append(a - b)
            elif current == "*" or current.lower() == "x":
                # product of two topmost values
                b = float(stack.pop())
                a = float(stack.pop())
                stack.append(a * b)
            elif current == "/":
                # (penultimate) over (topmost)
                b = float(stack.pop())
                a = float(stack.pop())
                stack.append(a / b)
            elif current == "^" or current == "**":
                # (penultimate) to the power of (topmost)
                b = float(stack.pop())
                a = float(stack.pop())
                stack.append(a ** b)
            elif current == "pi":
                # the all-famous diameter-circumference ratio constant!
                b = math.pi
                stack.append(b)
            elif current == "tau":
                # basically 2x pi
                b = 2 * math.pi
                stack.append(b)
            elif current == "e":
                # Euler's constant
                b = math.e
                stack.append(b)
            elif current == 'c':
                # speed of light
                b = 299792458
                stack.append(b)
            elif current == 'h':
                # Planck's constant
                b = 6.63e-34
                stack.append(b)
            elif current == "phi":
                # the golden ratio
                b = (2 + (5 ** 0.5))/2
                stack.append(b)
            elif current == "sin":
                # various trigonometric functions
                b = math.sin(stack.pop())
                stack.append(b)
            elif current == "asin":
                b = math.asin(stack.pop())
                stack.append(b)
            elif current == "cos":
                b = math.cos(stack.pop())
                stack.append(b)
            elif current == "acos":
                b = math.acos(stack.pop())
                stack.append(b)
            elif current == "tan":
                b = math.tan(stack.pop())
                stack.append(b)
            elif current == "atan":
                b = math.atan(stack.pop())
                stack.append(b)
            elif current == "%":
                # find remainder of (topmost) when divided by (penultimate)
                a = stack.pop()
                b = stack.pop()
                stack.append(b % a)
            elif current == "!":
                # factorial function
                b = stack.pop()
                if b % 1 == 0:
                    oj = b - 1
                    while oj > 0:
                        b *= oj
                        oj -= 1
                    stack.append(b)
                else:
                    error = "factorial must be integer"
                    raise BaseException()
                # there is, however, already math.factorial()...
            elif current == "log":
                # log base (penultimate) of (topmost)
                b = stack.pop()
                a = stack.pop()
                stack.append(math.log(a, b))
            elif current == "ans":
                # most recent answer calculated (from previous statement)
                b = ans
                stack.append(b)
            elif current == "sum":
                # sum of all currently stacked elements
                b = 0
                while len(stack) > 0:
                    b += stack.pop()
                stack.append(b)
            elif current == "product":
                # product of all currently stacked elements
                b = 1
                while len(stack) > 0:
                    b *= stack.pop()
                stack.append(b)
            elif current == "choose":
                # (penultimate)Choose(topmost) function
                b = stack.pop()
                a = stack.pop()
                b = math.factorial(a) / (math.factorial(b) * math.factorial(a - b))
                stack.append(b)
            elif current == "help":
                # help desk
                pass
            else:
                # else just stick it on the stack
                stack.append(float(current))
            oi += 1
        if len(stack) == 1:
            ans = float(stack[0])
            if droidMode:
                # This
                droid.setClipboard(str(ans))
            print(ans)
        else:
            error = "too many answers left"
            raise BaseException()
    except:
        print("Invalid expression, end result:")
        if error == 0:
            try:
                if b == 0 and current == "/" or a == 0 and b < 0 and current == "^":
                    error = "cannot divide by 0"
                elif a < 0 and abs(b) < 1 and current == "^":
                    error = "cannot root a negative"
                else:
                    error = "numbers not accepted"
            except:
                error = "unrecognised string"
        print(error)
        print(stack)