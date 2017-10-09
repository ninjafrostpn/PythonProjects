__author__ = 'Charlie'
import win32api as w

doneFactnos = w.GetProfileSection("Lowest number of (X) factors",
                                  "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
for x in range(0, len(doneFactnos)):
    bitweneed = int(doneFactnos[x].split("=")[0])
    doneFactnos[x] = bitweneed


doneFactoring = w.GetProfileSection("Factors of numbers",
                                    "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
for x in range(0, len(doneFactoring)):
    bitweneed = int(doneFactoring[x].split("=")[0])
    doneFactoring[x] = bitweneed


def findfactors(num):
    print("Finding factors of %s..." % num)
    i = 1
    factors = []
    while i <= num:
        if num % i == 0:
            factors.append(i)
        i += 1
    printlist(factors)
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
    if doneFactnos.count(no) > 0:
        return {"number": -2, "factors": [0]}
    else:
        i = 1
        while i < 10**100:
            if doneFactoring.count(i) > 0:
                i += 1
            else:
                factors = findfactors(i)
                factno = len(factors)
                if factno == int(no) and doneFactnos.count(factno) == 0:
                    return {"number": i, "factors": factors}
                elif doneFactnos.count(factno) == 0:
                    print("Number of %s factors (%s) as yet unrecorded!" % (factno, i))
                    w.WriteProfileVal("Lowest number of (X) factors",
                                      str(factno),
                                      str(i),
                                      "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
                    alerting(factno)
                    doneFactnos.append(factno)
                if doneFactoring.count(i) == 0:
                    print("Number %s's factors as yet unrecorded!" % i)
                    w.WriteProfileVal("Factors of numbers",
                                      str(i),
                                      printlist(factors, ", "),
                                      "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
                    doneFactoring.append(i)
                i += 1
        return {"number": -1, "factors": [0]}


def alerting(inputno):
    try:
        if inputno > max(doneFactnos):
            w.Beep(1000, 500)
            # input("Found new highest number of factors!")
        else:
            w.Beep(1500, 500)
    except:
        w.Beep(1500, 500)
        # input("First entry!")


try:
    print("Nos of factors already accounted for:")
    printlist(doneFactnos, ", ")
except:
    print("None as of yet")

try:
    print("Nos for which factors have been found:")
    printlist(doneFactoring, ", ")
except:
    print("None as of yet")


print("Begin factorisation of undone values...")
while True:
    numFacts = 1
    while numFacts <= 100:
        print("Finding number with %s factors..." % numFacts)
        numFound = firstoffactors(numFacts)
        if numFound["number"] == -1:
            print("Couldn't find one lower than a googol...")
        elif numFound["number"] == -2:
            print("already found number with %s factors" % numFacts)
        else:
            print("Lowest no. with %s factors is %s" % (numFacts, numFound["number"]))
            print("The factors were:")
            factorList = printlist(numFound["factors"], ", ")

            alerting(numFound["number"])
            w.WriteProfileVal("Lowest number of (X) factors",
                              str(numFacts),
                              str(numFound["number"]),
                              "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
            doneFactnos.append(numFacts)
            w.WriteProfileVal("Factors of numbers",
                              str(numFound["number"]),
                              factorList,
                              "E:\Program Files\Pycharm\Projects\\results_of_factoring.moo")
            doneFactoring.append(numFound["number"])
        numFacts += 1