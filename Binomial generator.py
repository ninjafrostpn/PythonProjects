__author__ = 'Charlie'
import random as rand
import math


def choose(n, r):
    if r > n:
        return False
    else:
        num = math.factorial(n)
        den = math.factorial(r) * math.factorial(n - r)
        return num / den


def arrangeTerm(coeffnum, coeffden, letter="X", exp=1.0, first=False):
    # turns the above data into a single string containing the term described
    # for shortness, prefix coeff stands for coefficient and suffixes -den and -num  for denominator and numerator
    term = ""
    if coeffnum < 0 and coeffden >= 0 or coeffnum >= 0 and coeffden < 0:
        # first, we see if the produced fractional coefficient would be negative (thus need a '-' sign)
        term += "- "
    elif not first:
        # (if first is true, the term is to be first in a line and so '+' signs are not required)
        term += "+ "
    if coeffden == 0:
        if coeffnum == 0:
            # with a 0/0, we got ourselves a nullity coefficient, thus nullity is our end value
            term = "+ NULLITY "
            return term
        else:
            # depending on the sign of our coefficient, sth/0 could mean + or - infinity as an end result
            term += "INFINITY "
            return term
    elif coeffnum == 0:
        # of course, 0/sth is otherwise just 0 as an end result (we keep the sign)
        term += "0 "
        return term
    elif coeffnum % coeffden == 0:
        # if the numerator divides evenly by the denominator (remainder of 0)
        # the coefficient can be simplified into a whole number
        if coeffnum / coeffden != 1:
            # unless, of course, it simplifies to 1, in which case why bother adding it in at all
            term += "%s" % int(abs(coeffnum / coeffden))
        elif exp == 0:
            # (here's why: if the X-ponent is 0...)
            term += "1 "
    else:
        # this seemingly complicated function takes the parts of our coefficient
        returnden = coeffden
        returnnum = coeffnum
        while True:
            # finds out what happens if you divide the denominator by the numerator
            factor = returnden / returnnum
            newcoeffden = returnden / factor
            newcoeffnum = returnnum / factor
            if int(factor) - factor == 0 and int(newcoeffnum) - newcoeffnum == 0 and int(newcoeffden) - newcoeffden == 0:
                # basically, if the coeff's num. and den. have an integer common factor
                # and they can both be evenly divided by it,
                # the coeff's num. and den. are simplified into a smaller equivalent fraction
                returnden = int(newcoeffden)
                returnnum = int(newcoeffnum)
            else:
                # if they don't, there's nothing we can do, so we move on
                break
        # to add this processed coefficient to our term
        term += "(%s/%s)" % (abs(int(returnnum)), abs(int(returnden)))
    if not isinstance(letter, type("A")):
        # if our X in aX^n is not a string...
        letter = "(%s)" % letter
    elif len(letter) != 1:
        # ...or it's not just one letter, we put it in brackets!
        letter = "(%s)" % letter
    if exp == 1:
        # let's be honest here, we don't need to display a to-the-power-of-1
        term += str(letter) + " "
    elif exp != 0:
        # and to-the-power-of-0 means no X in our aX^n at all!
        term += "%s^%s " % (str(letter), exp)
    return term

"""
print("TESTING: ",
      arrangeTerm(1, 3, "frog", 2, True),
      arrangeTerm(3, 1, "w", 3),
      arrangeTerm(6, 2, "q", 1),
      arrangeTerm(3, 0, "X", 4),
      arrangeTerm(0, 3, "D", 0.5),
      arrangeTerm(2, 4, "R", 12),
      arrangeTerm(0, 0, exp=2),
      arrangeTerm(1, 2, 304, 5),
      sep="")
"""

print("Example of input:"
      "\nQuestion:"
      "\n(4X^3 - (1/2))^2"
      "\nAnswer:"
      "\n1/4:0,-4:3,16:6"
      "\nWhich means:"
      "\n(1/4)X^0 or just 1/4"
      "\n- 4X^3"
      "\n+ 16X^6"
      "\nanswers don't have to be simplified, but they must be in this format without any spaces"
      "\ngenerally >> (sign)numerator(/denominator)(:power of X),(sign)numerator(/denominator)(:power of X),(...)"
      "\nbrackets indicate where something is not necessarily needed")

while True:
    power = rand.randrange(2, 7)

    Xponent = rand.randint(1, 5)
    Xcoeff = rand.randint(-20, 20)
    while Xcoeff == 0:
        Xcoeff = rand.randint(-20, 20)
    Xpart = arrangeTerm(Xcoeff, 1, "X", Xponent, True)

    Cden = rand.randint(1, 10)
    Cnum = rand.randint(-Cden, Cden)
    while Cnum == 0:
        Cnum = rand.randint(-10 * Cden, 10 * Cden)
    Cpart = arrangeTerm(Cnum, Cden, "C", 0)

    quest = "(%s %s)^%s" % (Xpart, Cpart, power)
    print(quest)

    # your answer here
    response = input("Input coefficients in ascending powers of X\n").split(",")
    yourAnswer = ""
    start = True
    if len(response) == power + 1:
        i = 0
        while i <= power:
            response[i] = response[i].split("/")
            if len(response[i]) == 2:
                response[i][1].split(":")
                if len(response[i][1]) == 2:
                    yourAnswer += arrangeTerm(int(response[i][0]),
                                              int(response[i][1][0]),
                                              "X",
                                              int(response[i][1][1]),
                                              start)
                else:
                    yourAnswer += arrangeTerm(int(response[i][0]),
                                              int(response[i][1][0]),
                                              "X",
                                              0,
                                              start)
            else:
                response[i][0].split(":")
                if len(response[i][0]) == 2:
                    print("WAAAH")
                    yourAnswer += arrangeTerm(int(response[i][0][0]),
                                              1,
                                              "X",
                                              response[i][0][1],
                                              start)
                else:
                    yourAnswer += arrangeTerm(int(response[i][0][0]),
                                              1,
                                              "X",
                                              0,
                                              start)
            i += 1
            start = False
        print(yourAnswer)
    else:
        print("Not enough answers?")

    # real answer worked out here
    realAnswer = arrangeTerm(Cnum ** power, Cden ** power, "X", 0, True)
    i = 1
    while i < power:
        RAnum = choose(power, i) * (Xcoeff ** i) * (Cnum ** (power - i))
        RAden = Cden ** (power - i)
        realAnswer += arrangeTerm(RAnum, RAden, "X", i * Xponent)
        i += 1
    realAnswer += arrangeTerm(Xcoeff ** power, 1, "X", Xponent * power)

    if yourAnswer == realAnswer:
        print("CORRECT")
    else:
        print("NOPE: ", realAnswer)