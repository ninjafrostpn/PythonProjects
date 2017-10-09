__author__ = 'Charlie'
from random import randint as rand

celebrations = ["Have a banana",
                "Give yourself a shiny!",
                "Nice job, Kowalski",
                "YAAAAAAAAAY!!!",
                "Da da-da-da-daaaaaaaaa",
                "Woohoo!",
                "SUCCESS",
                "And I don't even know how you did that..."]

things = []

class Thing:
    def __init__(self):
        self.name = input("Name\n>> ")
        self.desc = input("Details, please\n>> ")
        while True:
            try:
                self.rank = float(input("Priority\n>> "))
                break
            except:
                continue
        for i in range(0, len(things) + 1):
            if i == len(things):
                things.append(self)
                break
            elif things[i].rank > self.rank:
                continue
            elif things[i].rank == self.rank:
                if rand(0, 2) == 1:
                    continue
                else:
                    things.insert(i, self)
                    break
            else:
                things.insert(i, self)
                break

while True:
    whatdo = input("What?\n>> ").lower()
    if whatdo == "add":
        Thing()
    elif whatdo == "done":
        if len(things) > 0:
            whatdo = input("You have completed task: \"%s\" (%s)? (y/n)\n>> " %(things[0].name, things[0].desc)).lower()
            if whatdo[0] == "y":
                things.remove(things[0])
                print(celebrations[rand(0, len(celebrations))])
        else:
            print("...Done what, exactly?")
    elif whatdo == "list":
        for i in range(0, len(things)):
            if i == 0:
                print("LEVEL 1")
            elif i == 1:
                print("LEVEL 2")
            elif i == 4:
                print("LEVEL 3")
            print("%d: %s (%s) [%d]" % (i, things[i].name, things[i].desc, things[i].rank))
    elif whatdo == "view":
        if len(things) > 0:
            which = input("Which one?\n>> ")
            try:
                which = int(which)
                if which >= len(things):
                    raise "hell"
            except:
                print("So... the one you're doing?")
                which = 0
            print("%d: %s (%s) [%d]" % (which, things[which].name, things[which].desc, things[which].rank))
        else:
            print("...Nothing")
    elif whatdo == "exit":
        exit()