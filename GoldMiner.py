__author__ = 'Charlie'
from math import *

# ATTEMPT 1
"""
# the number of fibonacci numbers used in the denominator (it'll make sense, just read on)
depth = 1400  # int(input("Input depth of checking\n>> ")) # comment out to set as just number  # comments in comments

# generate the fibonacci numbers needed for later ease of access
a = 1
b = 1
fib = [a, b]
for i in range(depth - 2):
    a, b = b, a + b
    fib.append(b)

# and stick 'em in reverse order, 'cause that's how they're gonna be used
fib.reverse()

# g is Ak(x)... I just like that letter
g = float(input("Input g for trial\n>> "))

# now for the iterative formula
# g = x.F1 + (x^2).F2 + (x^3).F3 + (x^4).F4 + ...
# g/x = F1 + x.F2 + (x^2).F3 + (x^3).F4 + ... ('cause we can see x > 0 in the question)
# x = g/(F1 + x.F2 + (x^2).F3 + (x^3).F4 + ...)
# then do some weird stuff
# F1 + x.F2 + (x^2).F3 + (x^3).F4 + ... = F1 + x(F2 + x(F3 + x(F4 + x(...))))
# we could work backwards to get that same thing from some Fn and just disregard the final x(...) as tiny...
# Fn >> x(Fn) >> Fn-1 + x(Fn) >> x(Fn-1 + x(Fn)) >> Fn-2 + x(Fn-1 + x(Fn)) >> etc.
# which is what is going on here to get the denominator for the iterative formula
# ...so you get some value for x... and you go around again, working outward from Fn to get the denominator
# and get another x... 50 times seems to show something... see below


def itr8(xin, q, n=1):
    x = xin
    r = []
    for j in range(n):
        den = fib[0]
        for k in range(1, depth):
            den *= x
            den += fib[k]
        x = q/den
        r.append(x)
        # print(x)
    # print(r)
    return r


# on convergence of the iterative method:
# using 1000 terms of F(whatever) and 50 iterations, you can tell if the x is too high/low for the g as follows
# a number that is too high or too low will cause the sequence to oscillate between g and 0
# - if the number is higher than the true value for x, the final iteration will be g
# - if it's too low, then the final iteration will return 0
# if, however, it's spot on, it won't oscillate at all and will remain with the number you gave it
# for example, choose g to be 2 and then x to be 0.1, 20 or 0.5 and the following occurs
# 0.1                     23                      0.5
# ---------------------------------------------------
# 1.7799999999999998      0.0                     0.5
# 0.0                     2.0                     0.5
# 2.0                     0.0                     0.5
# 0.0                     2.0                     0.5
# 2.0                     0.0                     0.5
# 0.0                     2.0                     0.5
# ...                     ...                     ...
# 0.0                     2.0                     0.5
# 2.0                     0.0                     0.5
# 0.0                     2.0                     0.5
# 2.0                     0.0                     0.5
# 0.0                     2.0                     0.5
# trying this out with the other given number, 74049690, and 6 iterations the thing that seems to happen is:
# - enter x that is too small >1> really big number >2> 0 >3> g >4> 0 >5> g >6> 0
# - enter x that is too large >1> very small number >2> g >3> 0 >4> g >5> 0 >6> g
# but as you get closer to the true value for x, the first iteration for too-small/big numbers will produce
# a number that is less extreme (ie a smaller massive number and a larger small number respectively
# and the series will not descend into cyclic anarchy so quickly, so this means:
# - it's possible to tell when you're getting close by the change in extremeness of the first iteration
# - more iterations may be needed if you want to see the "last term" for closer numbers, so
# - it may be easier just to use the first iteration to tell which way you need to go to get to the true x

# iterative methods aside, the problem now is how to get a number for x in sufficient detail that we can tell
# whether it is rational
# almost certainly do negative feedback trial and error, but then... we could:
# - hope that they're all nice easy numbers like 0.5?
# - let it converge to a set no of DP then look at the denominator
# meh, let's try it

xmin = []
xmax = []
while True:
    xtest = 0  # float(input("Input x for start\n>> "))
    inc = 1
    count = 0
    prevx = -1
    while True:
        if prevx == xtest:
            count += 1
            if count >= 10:
                break
        else:
            count = 0
        result = itr8(xtest, g)[0]
        if result > xtest:
            prevx = xtest
            xtest += inc
        elif result < xtest:
            prevx = xtest
            xtest -= inc
            inc *= 0.1
        else:
            break
        # print(xtest)
    print("When g = %d, x = %s" % (g, str(xtest)))
    g += 1
"""

# ATTEMPT 2
# After that last attempt, I'm pretty sure that the xs we're looking for are in the nearabouts of 0.62
# So let's try the whole "p/q is a rational, plug in values, get rational answers" method
depth = 1476  # int(input("Input number of terms to sum\n>> "))
# generate the fibonacci numbers needed for later ease of access
while True:
    print("DEPTH = %s" % depth)
    try:
        a = 1
        b = 1
        fib = [a, b]
        for i in range(depth - 2):
            a, b = b, a + b
            fib.append(b)

        num = 1
        den = 1
        done = []
        while True:
            if num >= den - 1:
                num = 1
                den += 1
            else:
                num += 1
            hlfden = den/2
            x = num/den
            while num < hlfden or x in done or x <= 0.5 or x >= 0.64:
                if num >= den - 1:
                    num = 1
                    den += 1
                    hlfden = den/2
                else:
                    num += 1
                x = num/den
            done.append(x)
            # print(done)
            g = 0
            for i in range(depth):
                g += pow(x, i + 1) * fib[i]
            print("%d/%d = %s >> %s" % (num, den, x, g))
    except:
        depth -= 1