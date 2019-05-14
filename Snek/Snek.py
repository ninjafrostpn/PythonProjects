import pygame, time, math, os
from pygame.locals import *
import numpy as np
from random import randint as rand

# Initialise the pygame module
pygame.init()

# Width and Height of the game environment
w = 50
h = 50

# define colour 3-tuples
white = (255, 255, 255)
black = (0, 0, 0)
salmon = (200, 100, 100)
red = (255, 0, 0)

# Initialise the screen surface
screen = pygame.display.set_mode((10 * w, 10 * h))

# Initialise the font
filepath = os.path.dirname(os.path.realpath(__file__)) + "\\"
textfont = pygame.font.Font(filepath + "OpenSans-Regular.ttf", 12)

# Create all the text surfaces
space = textfont.render("PRESS SPACE TO START!", 0, white)
msg1_1 = textfont.render("*OM*", 0, white)
msg1_2 = textfont.render("*NOM*", 0, white)
msg2_1 = textfont.render("Heckin' close!", 0, white)
msg2_2 = textfont.render("Whoa!", 0, white)
msg2_3 = textfont.render("*BOOP*", 0, white)
msg2_4 = textfont.render("Careful, now!", 0, white)
msg3_1 = textfont.render("Ack!", 0, white)
msg3_2 = textfont.render("Ooch!", 0, white)
msg4_1 = textfont.render("Why, hello there", 0, white)
msg5_1 = textfont.render("'Scuse me", 0, white)
msg5_2 = textfont.render("Pardon me", 0, white)

# And place messages in a bank of messages
msgbank = {"nom": [msg1_1, msg1_2],
           "close": [msg2_1, msg2_2, msg2_3, msg2_4],
           "ouch": [msg3_1, msg3_2],
           "hello": [msg4_1],
           "excuse": [msg5_1, msg5_2]}

# obtain available channels
chanmax = pygame.mixer.get_num_channels()
print("Available channels: " + str(chanmax))
channels = [pygame.mixer.Channel(i) for i in range(chanmax)]

# Type of bgm to play: -1 is nothing, 0 is procedural, 1 is fixed
musicmode = 0

if musicmode == 0:
    # generates frequencies of sine wave so as to obtain a chromatic scale in either stereo channel
    Lwaves = []
    Rwaves = []
    for note in range(-24, 60):             # starts at 24 semitones below middle c, ends 59 above it
        notefreq = pow(2, note / 12) * 440  # magic formula for obtaining note frequencies
        # arrays of tuples of amplitudes of wave in either stereo channel
        Lwave = []
        Rwave = []
        samples = math.floor(22050 / notefreq)  # keeps number of wavecycles constant, not duration
        # actual waveform generation
        for i in range(100):
            for j in range(samples):
                theta = math.radians(j * (360 / samples))
                # alternating tracks: the first of each pair added goes to the left track, second to the right
                Lwave.append(int(1000 * math.sin(theta)))
                Lwave.append(0)
                Rwave.append(0)
                Rwave.append(int(1000 * math.sin(theta)))
        # reshapes the arrays into the correct form for reading as sound arrays
        Lwave = np.array(Lwave).reshape(100 * samples, 2)
        Rwave = np.array(Rwave).reshape(100 * samples, 2)
        # adds the waveforms to the appropriate arrays
        Lwaves.append(pygame.sndarray.make_sound(Lwave))
        Rwaves.append(pygame.sndarray.make_sound(Rwave))

    #tune = [8,8,10,12,8,12,10,3,8,8,10,12,8,8,7,
    #        3,8,8,10,12,13,12,10,8,7,3,5,7,8,8,8,8,
    #        5,7,5,3,5,7,8,5,3,5,3,1,0,0,3,3,
    #        5,7,5,3,5,7,8,5,3,8,7,10,8,8,8,8]

    # the correct intervals for the notes of scales
    major = [0, 2, 4, 5, 7, 9, 10]
    minor = [0, 2, 3, 5, 7, 8, 10]
elif musicmode == 1:
    # simply imports the given sound file to play during play
    music = pygame.mixer.Sound(filepath + "Wewewewewe.wav")


# Constrain function
def constrain(val, lo, hi):
    # Because these things are useful :)
    if val <= lo:
        return lo
    elif val >= hi:
        return hi
    else:
        return val


# class for segments, including the head
class segment:
    # given initial x,y position, the snek that they are part of and colour of previous segment
    def __init__(self, inix, iniy, snekin, colin=0):
        self.x = inix
        self.y = iniy
        self.body = snekin
        # Adds its coordinates to the end of the snek's list of segment coordinates
        self.body.coords.append((self.x, self.y))
        # gives the segment a random colour or, if given the previous segment's colour, one slightly different to that
        if colin == 0:
            self.col = [rand(0, 255), rand(0, 255), rand(0, 255)]
        else:
            r = rand(0, 2)
            self.col = [0, 0, 0]
            for i in range(3):
                if i == r:
                    self.col[i] = constrain(colin[i] + rand(-100, 100), 0, 255)
                else:
                    self.col[i] = colin[i]
        # this is the variable which stores the next segment in the snek if there is one
        self.next = 0

    # Displays the segment, given the coordinates that it's moving to (usually those of the previous segment)
    def show(self, xin, yin):
        if self.next != 0:
            # Shows the next segment before itself, so as to use the current coordinates
            self.next.show(self.x, self.y)
        self.x = xin
        self.y = yin
        # Draws a square where it is
        screen.fill(self.col, (self.x * 10, self.y * 10, 10, 10))

    # Adds extra segment by going along segments until it finds one which doesn't have a segment after it
    def extend(self, howmany):
        if howmany > 0:
            if self.next != 0:
                self.next.extend(howmany)
            else:
                self.next = segment(self.x, self.y, self.body, self.col)
                self.body.length += 1
                if musicmode == 0:
                    r = len(Rwaves)
                    while r > len(Rwaves) - 1:
                        r = rand(0, self.body.length)
                        r = (12 * int((r - (r % 7))/7)) + major[r % 7]
                    # print(r)
                    if self.body.side == 1:
                        self.body.tune.append(Rwaves[r])
                    elif self.body.side == 2:
                        self.body.tune.append(Lwaves[r])
                self.next.extend(howmany - 1)  # communicates to newly created segment that more need to be made


# The snek itself
class snek:
    # Takes initial x,y position of head and direction of travel, and the speaker through which its sound is played
    def __init__(self, inix, iniy, inidir=1, side=0):
        self.x = inix
        self.y = iniy
        self.movdir = inidir   # direction 0 is upward, clockwise around to 3 being left
        self.side = side  # works in binary; side 0 is neither, 1 is right, 2 is left, 3 is both
        self.length = 3  # number of segments of the snek
        self.coords = []  # coordinates of all the segments
        if musicmode == 0:
            self.tune = []  # the notes that the snek plays when moving
        # creates the snek
        self.head = segment(self.x, self.y, self) # create head
        self.head.extend(2)  # creates tail segments
        self.tunepos = 0
        # number of noms
        self.points = 0
        # variables used for control of actions
        self.turning = False  # Prevents double-turning which would allow head crashing into previous segment
        self.nommin = 0  # controls number of nom messages countdown
        self.msgs = []  # stores currently shown messages
        self.close = False  # recognises near misses

    # draws the snek
    def show(self):
        if self.side != 0 and musicmode == 0:
            channels[self.side].play(self.tune[self.tunepos])
            self.tunepos = (self.tunepos + 1) % len(self.tune)
        blockage = []
        for P in sneks:
            for C in P.coords:
                blockage.append(C)
        dead = False  # it is assumed that the snek has not crashed, until proven otherwise
        if self.movdir == 0:
            # Moving up
            self.y -= 1                                          # Changes y position
            if (self.x, self.y - 1) in blockage or self.y == 0:  #
                self.close = 2
        elif self.movdir == 1:
            # Moving right
            self.x += 1
            if (self.x + 1, self.y) in blockage or self.x + 1 == w:
                self.close = 2
        elif self.movdir == 2:
            # Moving down
            self.y += 1
            if (self.x, self.y + 1) in blockage or self.y + 1 == h:
                self.close = 2
        elif self.movdir == 3:
            # Moving left
            self.x -= 1
            if (self.x - 1, self.y) in blockage or self.x == 0:
                self.close = 2
        self.coords.pop()
        self.close -= 1
        if (self.x, self.y) in blockage or self.x >= w or self.x < 0 or self.y >= h or self.y < 0:
            self.say("ouch")
            print("OUCH!")
            dead = True
        elif self.close == 1:
            self.close = False
            self.say("close")
        self.coords.insert(0, (self.x, self.y))
        self.head.show(self.x, self.y)
        if len(self.msgs) > 0:
            for m in self.msgs:
                screen.blit(m[0], m[1])
            if rand(0, 1) == 1:
                self.msgs.pop()
        if self.nommin > 0:
            self.say("nom")
            self.nommin -= 1
        self.turning = False
        return dead

    def nom(self):
        growth = rand(1, 5)
        self.head.extend(growth)
        self.points += 1
        print("NOM #%s!" % self.points)
        self.nommin = 4

    def turn(self, newdir):
        if not self.turning and (newdir + self.movdir) % 2 != 0:
            self.movdir = newdir
            self.turning = True

    def say(self, msgtype):
        msgs = msgbank[msgtype]
        msg = msgs[rand(0, len(msgs) - 1)]
        msgx = constrain((10 * self.x) + rand(-20, 20) - (msg.get_width()/2), 0, (w * 10) - msg.get_width())
        msgy = constrain((10 * self.y) + rand(-20, 20) - (msg.get_height()/2), 0, (h * 10) - msg.get_height())
        self.msgs.append([msg, (msgx, msgy)])


def ai(A, targx, targy):
    if A.movdir == 0:
        if targx > A.x:
            return 1
        elif targx < A.x:
            return 3
        elif targy < A.y:
            pass
        elif targy > A.y:
            return [1, 3][rand(0, 1)]
    elif A.movdir == 1:
        if targy > A.y:
            return 2
        elif targy < A.y:
            return 0
        elif targx > A.x:
            pass
        elif targx < A.x:
            return [0, 2][rand(0, 1)]
    elif A.movdir == 2:
        if targx > A.x:
            return 1
        elif targx < A.x:
            return 3
        elif targy > A.y:
            pass
        elif targy < A.y:
            return [1, 3][rand(0, 1)]
    elif A.movdir == 3:
        if targy > A.y:
            return 2
        elif targy < A.y:
            return 0
        elif targx < A.x:
            pass
        elif targx > A.x:
            return [0, 2][rand(0, 1)]
    return A.movdir


def ai2(A, targx, targy):
    start = (A.x, A.y)
    finish = (targx, targy)
    grid = [(i, j) for j in range(h) for i in range(w)]
    for P in sneks:
        for C in P.coords:
            if C in grid and C != start:
                grid.remove(C)
    while start == finish:
        finish = grid[rand(0, len(grid) - 1)]
    if start in grid:
        cnxns = dict()
        for C in grid:
            routes = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if abs(i) != abs(j):
                        D = (C[0] + i, C[1] + j)
                        if D in grid:
                            routes.append(D)
            cnxns[C] = routes
        # print(cnxns)
        tlabels = dict()
        plabels = dict()
        tlabels[start] = [0, False]  # temporary weight, temporariness
        plabels[start] = [0, 0]  # permanent weight, labeling number
        order = 1
        while len(plabels) < len(cnxns) and finish not in list(plabels.keys()):
            for i in list(plabels.keys()):  # for location number already permalabeled
                for j in cnxns[i]:  # for location number connected to each of those
                    # if that location number is not also permalabeled
                    if j not in list(plabels.keys()):
                        # if it is already templabeled
                        if j in list(tlabels.keys()):
                            tlabels[j][0] = min(tlabels[j][0], plabels[i][0] + 1)  # if needed, give it a new label
                        # or else
                        else:
                            # label it for the first time
                            tlabels[j] = [plabels[i][0] + 1, True]
            best = [1000, -1]
            for i in list(tlabels.keys()):
                if tlabels[i][0] < best[0] and tlabels[i][1]:
                    best = [tlabels[i][0], i]
            if best[1] != -1:
                plabels[best[1]] = [best[0], order]
                tlabels[best[1]][1] = False
                order += 1
        print(plabels[finish][0], "Units:")
        path = [finish]
        weight = plabels[finish][0] - 1
        while weight >= 0:
            for i in cnxns[path[0]]:
                if i in list(plabels.keys()):
                    if plabels[i][0] == weight:
                        path.insert(0, i)
                        weight -= 1
                        break
        print(", ".join([str(i) for i in path]))
        next = path[1]
        if next[0] < start[0]:
            return 3
        elif next[0] > start[0]:
            return 1
        elif next[1] < start[1]:
            return 0
        elif next[1] > start[1]:
            return 2


# stores whether the nom, snek S, snek Z or music needs to be started
startup = [True, True, True, musicmode == 1]
inMenu = True  # stores whether in the menu or not
if musicmode == 0:
    # stores position in the procedural music track of either player
    Rcycle = 0
    Lcycle = 0

while True:
    if inMenu:
        screen.fill(black)
        screen.blit(space, (w * 3.7, h * 4.5))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == QUIT:
                quit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    exit()
                if e.key == K_SPACE:
                    inMenu = False
    else:
        if startup[0]:
            nomx = rand(0, w - 1)
            nomy = rand(0, h - 1)
            startup[0] = False
        if startup[1]:
            S = snek(10, 40, 1, side=1)
            startup[1] = False
        if startup[2]:
            Z = snek(40, 10, 3, side=2)
            startup[2] = False
        if startup[3]:
            channels[0].play(music, -1)
            startup[3] = False
        screen.fill(salmon)
        screen.fill(red, (nomx * 10, nomy * 10, 10, 10))
        sneks = [S, Z]
        startup[1] = S.show()
        startup[2] = Z.show()
        if (S.x, S.y) == (nomx, nomy):
            S.nom()
            startup[0] = True
        elif (Z.x, Z.y) == (nomx, nomy):
            Z.nom()
            startup[0] = True
        pygame.display.flip()
        #S.turn(ai2(S, nomx, nomy))
        #Z.turn(ai(Z, nomx, nomy))
        for e in pygame.event.get():
            if e.type == QUIT:
                quit()
            elif e.type == KEYDOWN:
                if e.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                    S.turn({K_UP:0, K_RIGHT:1, K_DOWN:2, K_LEFT:3}[e.key])
                elif e.key in [K_w, K_a, K_s, K_d]:
                    Z.turn({K_w:0, K_d:1, K_s:2, K_a:3}[e.key])
                elif e.key == K_ESCAPE:
                    exit()
        time.sleep(0.07)
