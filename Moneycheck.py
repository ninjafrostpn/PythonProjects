import os
import time

filepath = "C:\\Users\\Charles Turvey\\Documents\\Money\\"
print(filepath)

reserves = dict()
files = dict()


def openreserve(name, createnew=True):
    while True:
        try:
            try:
                print("- Attempting to open %s" % name)
                file = os.open(filepath + name + ".casct", os.O_APPEND | os.O_RDWR)
            except FileNotFoundError:
                if createnew:
                    print("- ...Creating %s first" % name)
                    file = os.open(filepath + name + ".casct", os.O_APPEND | os.O_RDWR | os.O_CREAT)
                    os.write(file, bytes("Transaction,In,Total,Date,Details", "UTF-8"))
                    os.close(file)
                    file = os.open(filepath + name + ".casct", os.O_APPEND | os.O_RDWR)
                else:
                    print("- File not found")
                    return False
            break
        except PermissionError:
            input("YOU MUST CLOSE THE FILE FIRST!\nPress Enter to try again. >> ")
    print("- Opened %s" % name)
    print("- Reading from file")
    raw = ""
    while True:
        part = str(os.read(file, 100))[2:-1]
        # print(part)
        if part == "":
            break
        else:
            raw += part
    print("- Interpreting file data")
    reserves[name] = [i.split(",") for i in raw.split(";")]
    files[name] = file
    return True


def addrow(name, item, amt, when):
    try:
        total = reserves[name][-1][2]
        transaction = reserves[name][-1][0]
    except KeyError:
        openreserve(name)
        # print(reserves[name])
        total = reserves[name][-1][2]
        transaction = reserves[name][-1][0]
    if total == "Total":
        # print(reserves[name])
        total = 0
        transaction = 0
    else:
        total = float(total)
        transaction = int(transaction)
    if when.lower() in ["", "now"]:
        when = time.strftime("%Y%m%dGMT", time.gmtime())
    row = [str(transaction + 1), str(round(float(amt), 3)), str(round(total + float(amt), 3)), when, str(item)]
    # print(row)
    reserves[name].append(row)
    os.write(files[name], bytes(";" + ",".join(row), "UTF-8"))


def addmoneys(amt, dest):
    reason = input("Why was %s added to %s?\n>> " %(amt, dest))
    when = input("When was this?\n>> ")
    addrow(dest, reason, amt, when)
    print("- Added £%s to %s" % (amt, dest))


def removemoneys(amt, orig):
    reason = input("Why was %s removed from %s?\n>> " % (amt, orig))
    when = input("When was this?\n>> ")
    addrow(orig, reason, -amt, when)
    print("- Removed £%s from %s" % (amt, orig))


def transfermoneys(amt, orig, dest):
    reason = input("Why was %s transferred from %s to %s?\n>> " % (amt, orig, dest))
    when = input("When was this?\n>> ")
    addrow(orig, reason, -amt, when)
    addrow(dest, reason, amt, when)
    print("- Transferred £%s from %s to %s" % (amt, orig, dest))

while True:
    command = input("Input command\n>> ").lower().split()
    while len(command) > 0:
        word = command.pop(0)
        if word == "add":
            amt = float(command.pop(0))
            dest = command.pop(0)
            if dest == "to":
                dest = command.pop(0)
            if amt < 0:
                removemoneys(-amt, dest)
            else:
                addmoneys(amt, dest)
        elif word == "remove":
            amt = float(command.pop(0))
            orig = command.pop(0)
            if orig == "from":
                orig = command.pop(0)
            if amt < 0:
                addmoneys(-amt, orig)
            else:
                removemoneys(amt, orig)
        elif word == "transfer":
            amt = float(command.pop(0))
            orig = command.pop(0)
            if orig == "from":
                orig = command.pop(0)
            dest = command.pop(0)
            if dest == "to":
                dest = command.pop(0)
            if amt < 0:
                orig, dest = dest, orig
                amt = -amt
            transfermoneys(amt, orig, dest)
        elif word == "shop":
            location = command.pop(0)
            if location == "at":
                location = command.pop(0)
            reserve = command.pop(0)
            if reserve == "using":
                reserve = command.pop(0)
            when = input("When did you go?\n>> ")
            while True:
                item = input("Input item\n>> ")
                if item == "":
                    break
                price = float(input("Input price\n>> "))
                addrow(reserve, "Bought %s at %s" % (item, location), -price, when)
        elif word == "view":
            name = command.pop(0)
            try:
                for row in reserves[name]:
                    output = ""
                    for item in row:
                        output += item + (" " * (15 - len(item)) * (len(item) < 15))
                    print(output)
            except KeyError:
                if openreserve(name, False):
                    for row in reserves[name]:
                        output = ""
                        for item in row:
                            output += item + (" " * (15 - len(item)) * (len(item) < 15))
                        print(output)
                else:
                    print("No such thing available")
        elif word == "spam":
            name = command.pop(0)
            for i in range(50):
                addmoneys(i, name)
        elif word == "exit":
            exit()
        else:
            print("Eh?")
