"""
__author__ = 'Charlie'
while True:
    penv = float(input("Give density (kgm^-3) of environment\n>> "))
    vtot = float(input("Give volume (m^3) of container\n>> "))
    p1 = float(input("Give density (kgm^-3) of material 1\n>> "))
    p2 = float(input("Give density (kgm^-3) of material 2\n>> "))

    v1 = (vtot * (penv - p2))/(p1 - p2)
    v2 = vtot - v1
    ptot = ((v1 * p1) + (v2 * p2))/vtot

    print("%s m^3 of material 1 and\n%s m^3 of material 2\nrequired for neutral buoyancy" % (v1, v2))
    print("Gives density of %s kgm^-3\n" % ptot)
"""

import math as m
import string
digs = "0123456789abcdefghijklmnopqrsuv"

def base(x):
    base = len(digs)
    if x < 0:
        x *= -1
        sign = "-"
    elif x == 0:
        return "0"
    else:
        sign = ""
    i = 0
    j = []
    while x > 0:
        q = (x % pow(base, i+1))
        #print(q)
        x -= q
        j.append(digs[int(q/pow(base, i))])
        i += 1
    j.reverse()
    return sign + "".join(j)

code = ""
mu = 0
sigma = 20
for i in range(0, 360 * 12):
    theta = (i/180) * m.pi
    code += base(-50 + 50*i) + " "
    code += base(50 + round(5000 * m.sin(m.radians(i)))) + " "
code += "##"
print(code)