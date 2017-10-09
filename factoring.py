__author__ = 'Charlie'
import win32api as w

def findfactors(num):
    i = 1
    factors = []
    while i <= num:
        if num % i == 0:
            factors.append(i)
        i += 1
    printlist(factors)
    print("")
    return factors


def printlist(thinglist, sep="\n"):
    if isinstance(thinglist, type([1])):
        i = 0
        printstr = ""
        while i < len(thinglist) - 1:
            printstr += str(thinglist[i]) + sep
            i += 1
        printstr += str(thinglist[i])
        print(printstr)
        return printstr
    else:
        print("To print a list, input a list...")


def firstoffactors(no):
    alreadythere = w.GetProfileVal("Lowest number of (X) factors",
                                   no,
                                   -1,
                                   "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
    if alreadythere == -1:
        i = 1
        while i < 10**100:
            factors = findfactors(i)
            factno = len(factors)
            if factno == int(no):
                return {"number": i, "factors": factors}
            i += 1
        return [-1, 0]
    else:
        i = alreadythere
        factors = w.GetProfileVal("Factors of numbers",
                                  str(i),
                                  "-1",
                                  "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo").split(", ")
        return {"number": i, "factors": factors}

while True:
    numFacts = input("Input number of factors required, we'll find the lowest no. with that many\n")
    numFound = firstoffactors(numFacts)
    if numFound["number"] == -1:
        print("Couldn't find one lower than a googol...")
    else:
        print("Lowest no. with %s factors is %s" % (numFacts,numFound["number"]))
        print("The factors were:")
        factorList = printlist(numFound["factors"],", ")

        w.WriteProfileVal("Lowest number of (X) factors",
                          str(numFacts),
                          str(numFound["number"]),
                          "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
        w.WriteProfileVal("Factors of numbers",
                          str(numFound["number"]),
                          factorList,
                          "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")