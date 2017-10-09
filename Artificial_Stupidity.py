from random import randrange, randint
from math import sin, pi, sqrt
import colorama as c
c.init()

maxwidth = 77
maxheight = 58

xsquares = 70     # width...
ysquares = 30     # ...and height (squares) of the environment
minDur = 500     # how long a "minute" lasts (ms)
debug = False
critters = []
startCritNo = 20
critterNo = 0
critterTot = 0
pos = lambda x, y: '\x1b[%d;%dH' % (y, x)
activity = []


def constrain(val, hi, lo):
    if val >= hi:
        return hi
    elif val <= lo:
        return lo
    else:
        return val


def breakup(whole, fraglen):
    fragments = []
    m = 0
    while m < len(whole):
        fragment = ""
        n = 0
        while n < fraglen and m < len(whole):
            fragment += whole[m]
            m += 1
            n += 1
        fragments.append(fragment)
    return fragments


def logger(words="", breaker="\n"):
    splitWords = words.split(breaker)
    for w in range(0, len(splitWords)):
        if len(splitWords[w]) > maxwidth:
            splitWord = breakup(splitWords[w], maxwidth)
            for u in range(0, len(splitWord)):
                activity.append(splitWord[u])
        else:
            activity.append(splitWords[w])
        while len(activity) > maxheight - ysquares:
            activity.pop(0)


def showlog():
    for w in range(0, len(activity)):
        sparespace = maxwidth - len(activity[w])
        print(c.Back.WHITE + c.Fore.BLACK + pos(1, ysquares + w + 1) + activity[w] + (" " * sparespace))


# takes args defining: "unique" (doesn't have to be) name for ID
#                      x and y values for initial positioning on the grid (downright from top left)
#                      the number of "seconds" (in-program cycles) which must pass between when each gene on its DNA
#                          is activated
#                      the (max)number of coded letters to use in each gene when splitting DNA for reading
#                          its DNA code for movement, action and so on
# You may notice that the terms used here are incorrect, since its DNA is only one gene and the so-called genes are
#     akin to codons of information, and are so named here
# yes, there are inconsistencies, but this is fun research, not a scientifically viable alternative to life... that
#     would sacrilegious and wrong
class Critter:
    def __init__(self, nameset, 
                 xset="%", yset="%", 
                 speedset="%", longset="%", periodset="%", 
                 readset="%", codonset="%", DNAset="%", idset=critterTot):
        # x, y, oldX, oldY, step, period, readDir, codon, speed, energy, age, eating, id
        # the integer ID here is unique for every critter in one session
        # longevity
        # name, lifeStage, DNA
        # breeding, reproducing

        # the x, y and speed values are merely set as expected
        if xset == "%":
            self.x = randint(0, xsquares)
        else:
            self.x = xset
        if yset == "%":
            self.y = randint(0, ysquares)
        else:
            self.y = yset
        self.oldX = self.x
        self.oldY = self.y
        if speedset == "%":
            self.speed = randint(-5, 6)
        else:
            self.speed = speedset
        # this variable keeps an eye on which point through the DNA read we are
        self.step = 0
        # the period, in steps, between gene reads is also just set from the provided value 
        #     (unless it's 0, since no genes would be read as we'll see later)
        if periodset == "%":
            # randomly set period from 1-10
            self.period = randint(1, 11)
            if self.period == 0:
                # just to double-check...
                self.period = 1
        elif periodset == 0:
            self.period = 1
        else:
            self.period = abs(periodset)
        # direction in which genes are read is set
        if readset == "%":
            # 1 in 2 chance of reverse read direction
            if 1 == randint(0, 2):
                self.readDir = -1
            else:
                self.readDir = 1
        elif readset < 0:
            self.readDir = -1
        else:
            self.readDir = 1
        # here, the length of DNA read after each period of waiting is set
        if codonset == "%":
            # DNA codon length of 1-5
            self.codon = randint(1, 6)
        else:
            self.codon = constrain(codonset, 1, 5)
        # and, of course, so are perhaps the most important parts, the "unique" identifier for the Critter...
        self.name = nameset
        # ...and its instructions for life
        if DNAset == "%":
            # random DNA code generation (up to 10 codons long)
            DNAlen = randint(self.codon, (self.codon * 10) + 1)
            letterbox = []
            for i in range(0, DNAlen):
                addition = str(chr(randint(ord('a'), ord('z') + 1)))
                if 1 == randint(0, 2):
                    addition = addition.upper()
                letterbox.append(addition)
            self.DNA = "".join(letterbox)
        else:
            self.DNA = DNAset
        # this one tells any nearby critters that it will breed if possible
        self.breeding = False
        self.reproducing = False
        # records how well-fed the critter is (percentage)
        self.energy = 100
        # and its attack levels (or something)
        self.eating = 0
        # and how old
        self.age = 0
        self.lifeStage = "Juvenile"    # these go: Juvenile, Adult, Elder
        if longset == "%":
            # sets how long it takes for a critter to reach the next stage (in years)
            self.longevity = 0
            while self.longevity == 0:
                self.longevity = randrange(0, 5)
        else:
            self.longevity = constrain(longset, 0.001, 5)
        self.id = idset
        data = "Name{" + self.name + "} ID{" + str(self.id) + \
               "} (x,y){" + str(self.x) + "," + str(self.y) + \
               "} Speed{" + str(self.speed) + "} Period{" + str(self.period) + \
               "} Codon{" + str(self.codon) + "} Dir{" + str(self.readDir) + "} DNA{" + self.DNA + \
               "} Lngvty{" + str(self.longevity) + "}"
        logger(data)

    def next(self, act):
        if debug:
            logger("updating " + self.name + " (" + str(act) + ", " + str(self.period) + ")")
        # the critter gets older
        self.age += 1
        if self.age % int(14400 * self.longevity) == 0:
            if self.lifeStage == "Juvenile":
                self.lifeStage = "Adult"
            elif self.lifeStage == "Adult":
                self.lifeStage = "Elder"
        # according to the number that is presented to it ("minutes" since session began),
        #     the Critter may act if <a multiple of it's period between actions>"minutes" has passed
        if self.period == 0:
            # more double-checking...
            self.period = 1
        if act % abs(self.period) == 0:
            if debug:
                logger(self.name + " activated")
            self.oldX = self.x
            self.oldY = self.y
            self.reproducing = False
            # regardless of whether or not it does anything, it still loses energy
            self.energy -= 1
            # at which point, it splits up the DNA into codons according to the length of codon it currently has stored
            DNAread = []
            gene = ""
            # DNA read in correct direction according to readDir
            DNAlen = len(self.DNA)
            if self.readDir > 0:
                base = ""
                for i in range(0, DNAlen):
                    j = 0
                    while j < self.codon and i < DNAlen:
                        base += self.DNA[i]
                        i += 1
                        j += 1
                    DNAread.append(base)
                    base = ""
                gene += DNAread[self.step]
            else:
                base = ""
                for i in range(0, DNAlen):
                    j = 0
                    while j < self.codon and i < DNAlen:
                        base += self.DNA[len(self.DNA) - (i + 1)]
                        i += 1
                        j += 1
                    DNAread.append(base)
                    base = ""
                gene += DNAread[len(DNAread) - (self.step + 1)]
            if debug:
                logger("read gene[" + gene + "]:")
            i = 0
            xup = 0
            yup = 0
            periodup = 0
            reverse = 1
            speedup = 0
            mustdark = False
            mustlight = False
            mustyoung = False
            mustold = False
            mustsee = False
            mustavoid = False
            eat = 0
            breed = 0
            unused = 0
            while i < len(gene):
                base = gene[i]
                if debug:
                    logger("(read base[" + base + "])")
                # having read the correct DNA char, the critter acts accordingly
                if base == 'N':        # NESW and nesw code for compass-point directions
                    yup -= 1
                elif base == 'E':
                    xup += 1
                elif base == 'S':
                    yup += 1
                elif base == 'W':
                    xup -= 1
                elif base == 'n':
                    yup -= 1
                elif base == 'e':
                    xup += 1
                elif base == 's':
                    yup += 1
                elif base == 'w':
                    xup -= 1
                elif base == 'l':                # l for "light low" condition (read actions won't happen in high light)
                    mustdark = True
                elif base == 'L':                # L for "light high" condition (read actions won't happen in low light)
                    mustlight = True
                elif base == 'p':                # p for "period down" action (decreases inter-codon read period)
                    periodup -= 1
                elif base == 'P':                # P for "period up" action (increases inter-codon read period)
                    periodup += 1
                elif base == 'R':                # R for "reverse read" action (reverses codon read direction)
                    reverse *= -1
                elif base == 'a':                # a for "attack less" action (stops eating but can be cancelled by A)
                    eat -= 1
                elif base == 'A':                # A for "attack more" action (starts eating)
                    eat += 1
                elif base == 'b':                # b for "breed less" action (stops breeding by cancelling out B)
                    breed -= 1
                elif base == 'B':                # B for "breed more" action (starts breeding unless cancelled by b)
                    breed += 1
                elif base == 'v':                # v for "velocity down" action (decreases distance multiplier)
                    speedup -= 1
                elif base == 'V':                # V for "velocity up" action (increases distance multiplier)
                    speedup += 1
                elif base == 'Y':                # Y for "younger critter"
                    mustyoung = True
                elif base == 'O':                # O for "older critter"
                    mustold = True
                elif base == 'd':                # d for "don't detect", works as inverse of below
                    mustavoid = True
                elif base == 'D':                # D for "detect others" (range from no. of unused codon letters + 1)
                    mustsee = True
                else:                            # counts unused letters
                    unused += 1
                i += 1
            # check if it wants certain light levels or age rating
            exprdark = (mustdark and light == "Low") or not mustdark
            exprlight = (mustlight and light == "High") or not mustlight
            exprlim = mustdark and mustlight and light == "Liminal"
            expryoung = (mustyoung and self.lifeStage == "Juvenile") or not mustyoung
            exprold = (mustold and self.lifeStage == "Elder") or not mustold
            exprmiddle = mustyoung and mustold and self.lifeStage == "Adult"
            # this section checks to see if there are any critters lurking within the radius
            #     given by the number of unused letters
            detected = False
            for i in range(0, len(critters)):
                if critters[i].id != self.id:
                    if sqrt(((self.x - critters[i].x) ** 2) + ((self.y - critters[i].y) ** 2)) <= unused + 1:
                        if debug:
                            logger(critters[i].name + " was seen by " + self.name)
                        detected = True
                        break
            exprsee = (mustsee and detected) or not mustsee
            expravoid = ((mustavoid and not detected) or not mustavoid)
            expressit = (exprdark and exprlight or exprlim) and \
                        ((expryoung and exprold) or exprmiddle) and \
                        (exprsee and expravoid)

            if expressit:
                # speed can be any integer 'tween 5 and -5 inclusive
                self.speed = constrain(self.speed + speedup, -5, 5)
                # and the speed change is taken into account before moving by the amount given
                self.x += xup * self.speed
                self.y += yup * self.speed
                if debug:
                    logger(self.name + " went " + str(xup * self.speed) + " along and "
                           + str(yup * self.speed) + " down")
                # the period determines two things
                #         -its magnitude determines the length of wait in "minutes" between a critter's codon reads
                #         -its sign indicates the direction in which codons are read
                #             (-ve for right-to-left, +ve for left-to-right)
                # unlike speed, period has no size limit
                self.period += periodup
                if self.period < 0:
                    self.period = 1
                # reverses read direction if required
                self.readDir *= reverse
                if breed > 0:
                    self.breeding = True
                    # reproducing = False
                else:
                    self.breeding = False
                    # reproducing = False
                if eat > 0 and not self.breeding:
                    self.eating += eat
                else:
                    self.eating = 0
            # ensures that the critter cannot go out of bounds
            while self.x < 1:
                self.x += xsquares
            while self.y < 1:
                self.y += ysquares
            if self.x > xsquares:
                self.x -= xsquares
            if self.y > ysquares:
                self.y -= ysquares
            self.step = (self.step + 1) % len(DNAread)
            if debug:
                data = {"data for", self.name, "(" + self.id + ") after update\n (x,y)", str(self.x), str(self.y),
                        "(p,d)", str(self.period), str(self.readDir), "(cdln)", str(self.codon), "(V)", str(self.speed),
                        "(e)", str(self.energy), "(age)", str(self.age), self.lifeStage, "(pow)", str(self.eating),
                        "(brd?)", str(self.breeding), str(self.reproducing)}
                logger(" ".join(data) + "\n")

    def unshow(self):
        print(pos(self.oldX, self.oldY) + timecol + " ")

    def show(self):
        col = pos(self.x, self.y) + c.Back.WHITE
        if self.breeding:
            col += c.Fore.GREEN
        elif self.eating > 0:
            col += c.Fore.RED
        else:
            col += c.Fore.BLUE
        print(col + self.name[0])

    def newLife(self, partner):
        newname = self.name + partner.name + str(critterTot)
        if len(newname) > 5:
            newname = newname[0: 5]
        if randint(0, 2) == 1:
            newx = self.x
            newy = self.y
        else:
            newx = partner.x
            newy = partner.y
        newspeed = constrain(int(((self.speed + partner.speed) / 2) + randrange(-1, 2)), -5, 5)
        newreadDir = self.readDir * partner.readDir
        if randint(0, 2) == 1:
            newreadDir *= -1
        newperiod = abs(int(((self.period + partner.period) / 2) + randrange(-1, 2)))
        if newperiod == 0:
            # just to double-check...
            newperiod = 1
        # DNA codon length of 1-3
        newcodon = constrain(abs(int(((self.codon + partner.codon) / 2) + randrange(-1, 2))), 1, 5)
        # random DNA code generation (up to 10 codons long)
        if len(self.DNA) >= len(partner.DNA):
            DNA1 = self.DNA
            DNA2 = partner.DNA
        else:
            DNA1 = partner.DNA
            DNA2 = self.DNA
        DNAlen = constrain(int(((len(DNA1) + len(DNA2)) / 2) + randrange(-len(DNA1), len(DNA2))), 1, 50)
        letterbox = []
        for i in range(0, DNAlen):
            letterbox = []
            if 1 == randint(0, 2):
                addition = DNA1[i % len(DNA1)]
            else:
                addition = DNA2[i % len(DNA2)]
            if 1 == randint(0, 5):
                addition = str(addition).upper()[0]
            elif 1 == randint(0, 5):
                addition = str(addition).lower()[0]
            if 1 == randint(0, 5):
                if str(addition).lower() == str(addition):
                    addition = chr(constrain(int(ord(addition) + randrange(-1, 2)), ord('a'), ord('z')))
                else:
                    addition = chr(constrain(int(ord(addition) + randrange(-1, 2)), ord('A'), ord('Z')))
            letterbox.append(str(addition))
        newDNA = "".join(letterbox)
        # sets how long it takes for a critter to reach the next stage (in years)
        newlongevity = 0
        while newlongevity <= 0:
            newlongevity = constrain(((self.longevity + partner.longevity) / 2) + randrange(-1, 2), 0.001, 5)
        self.reproducing = True
        critters.append(Critter(newname, newx, newy, newspeed, newlongevity, newperiod,
                                newreadDir, newcodon, newDNA, critterTot))
        return newname

    def reproduced(self):
        self.reproducing = True

# Setup begins here
if debug:
    # name, x, y, period, longevity, DNA read direction, codon length, DNA String
    # critters.add(new Critter("§", 10, 5, 1, 1, 1, 1, 3, "OYW"))
    critters.append(Critter("£", 7, 3, 1, 1, 1, 1, 1, "BE", critterTot))
    critters.append(Critter("§", 5, 4, 1, 0.01, 1, 1, 1, "BWW", critterTot))
    critterTot += 2
    critterNo += 2
else:
    for i in range(0, startCritNo):
        # creates the determined number of critters named alphabetically
        critters.append(Critter(str(chr((critterNo % 26) + ord('A'))), idset=critterTot))
        critterTot += 1
        critterNo += 1


minute = 1
hour = 1
day = 1
month = 1
time = "Day"
season = "Summer"
timecol = ""

while True:
    if season == "Autumn":
        r = 173
        g = 105
        b = 64
    elif season == "Winter":
        r = 0
        g = 208
        b = 237
    elif season == "Spring":
        r = 123
        g = 243
        b = 102
    elif season == "Summer":
        r = 255
        g = 90
        b = 102
    lightLevel = constrain(int(50 * sin(((2 * pi)/(60 * 24)) * (minute % (60 * 24)))),
                           -int(sin(pi/2) * 50), int(sin(pi/2) * 50))
    lightLevel += 50
    if lightLevel >= 66:
        light = "High"
    elif lightLevel >= 33:
        light = "Liminal"
    else:
        light = "Low"
    # update all critters according to what's going on
    for i in range(0, len(critters)):
        critters[i].next(minute)
    # eating checks to see if anyone can breed with/eat anyone
    ignore = 0
    i1 = 0
    while i1 < critterNo - ignore:
        if critters[i1].breeding and not critters[i1].reproducing:
            i2 = 0
            while i2 < critterNo - ignore:
                if critters[i1].id != critters[i2].id and (critters[i1].x >= critters[i2].x - 1) and (critters[i1].y >= critters[i2].y - 1) and (critters[i1].x <= critters[i2].x + 1) and (critters[i1].y <= critters[i2].y + 1) and (critters[i2].breeding or (critters[i2].eating == 0)) and not critters[i2].reproducing:
                    babyname = critters[i1].newLife(critters[i2])
                    critterTot += 1
                    critterNo += 1
                    logger(critters[i1].name + " and " + critters[i2].name + " spawned a baby! Welcome " + babyname)
                    critters[i1].reproduced()
                    critters[i2].reproduced()
                    # prevents endless inbreeding loop
                    ignore += 1
                i2 += 1
        elif critters[i1].eating > 0:
            i2 = 0
            while i2 < critterNo:
                if (critters[i1].id != critters[i2].id) and \
                        (critters[i1].x >= critters[i2].x - 1) and (critters[i1].y >= critters[i2].y - 1) \
                        and (critters[i1].x <= critters[i2].x + 1) and (critters[i1].y <= critters[i2].y + 1):
                    if critters[i1].eating > critters[i2].eating:
                        logger(critters[i2].name + " was eaten by " + critters[i1].name)
                        critters.pop(i2)
                        if i1 > i2:
                            i1 -= 1
                        i2 -= 1
                        critterNo -= 1
                    elif critters[i1].eating < critters[i2].eating:
                        logger(critters[i1].name + " was eaten by " + critters[i2].name)
                        critters.pop(i1)
                        i1 -= 1
                        if i2 > i1:
                            i2 -= 1
                        critterNo -= 1
                i2 += 1
        i1 += 1
    
    # colour everything in
    ##############################
    lightR = int((lightLevel * r)/100)
    lightG = int((lightLevel * g)/100)
    lightB = int((lightLevel * b)/100)
    prevcol = timecol
    if lightLevel == "Low" or (lightLevel == "Liminal" and time == "Night"):
        timecol = c.Back.BLACK
    else:
        if season == "Summer":
            timecol = c.Back.RED
        elif season == "Spring":
            timecol = c.Back.GREEN
        elif season == "Autumn":
            timecol = c.Back.MAGENTA
        elif season == "Winter":
            timecol = c.Back.CYAN
        else:
            timecol = c.Back.WHITE
    # background(lightR, lightG, lightB)
    # fill(lightR, lightG, lightB)
    if prevcol != timecol:
        for j in range(0, ysquares + 1):
           print(c.Style.RESET_ALL + pos(0, j) + (" " * xsquares))
    # fill(255 - lightG, 255 - lightB, 255 - lightR)
    output = {"mmhhddMM:", str(minute), str(hour), str(day), str(month), 
                        "}\nSeason:", season, time, 
                        "}\nLightlevel:", str(lightLevel), light, 
                        "}\nRGB:", str(lightR), str(lightG), str(lightB), "}",
                        "}\nPopulation:", str(critterNo), "}"}
    # text("".join(output), 0, gridsize)
    for i in range(0, len(critters)):
        critters[i].unshow()
    for i in range(0, len(critters)):
        critters[i].show()
    showlog()

    # wait
    for i in range(0, minDur * 1000):
        pass
    
    # increment all timers
    minute += 1
    if minute % 60 == 0:
        hour += 1
        if hour % 12 == 0:
            if time == "Day":
                time = "Night"
            else:
                time = "Day"
                day += 1
                if day % 10 == 0:
                    month += 1
                    if season == "Summer":
                        season = "Autumn"
                    elif season == "Autumn":
                        season = "Winter"
                    elif season == "Winter":
                        season = "Spring"
                    elif season == "Spring":
                        season = "Summer"

# python "E:\Program Files\Pycharm\Projects\Artificial_Stupidity.py"