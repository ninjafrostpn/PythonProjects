import pygame
from pygame.locals import *
from math import atan2, degrees, radians, copysign, pi, sin, cos
from random import shuffle, randrange
from time import sleep

debugmode = False

screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()
screenrect = screen.get_rect()

wallthickness = 10

obstacles = []
things = []
players = []


# Handy constrain function
def constrain(val, lo, hi):
    return min(max(val, lo), hi)


# Handy pythagorean function
def pythag(a, b):
    return ((a ** 2) + (b ** 2)) ** 0.5


# Debug printing
def qrint(*args):
    if debugmode:
        print(*args)


# Generates a hitbox for the given sprite at given position, with scaled image offset
def generatehitbox(x, y, sprite, scaledoffset=(0.5, 0.5)):
    sx = sprite.get_width()
    sy = sprite.get_height()
    return Rect(x - (sx * scaledoffset[0]), y - (sy * scaledoffset[1]), sx, sy)


# Standard AI
def AI(selfpos, goalpos, ballpos, force, col):
    dx = goalpos[0] - ballpos[0]
    dy = goalpos[1] - ballpos[1]
    d = pythag(dx, dy)
    if d == 0:
        targx, targy = ballpos
    else:
        targx = ballpos[0] - (20 * (dx / d))
        targy = ballpos[1] - (20 * (dy / d))
    if debugmode:
        pygame.draw.circle(screen, col, (int(targx), int(targy)), 10)
    ang = atan2(targy - selfpos[1], targx - selfpos[0])
    return (force * (cos(ang) + randrange(-1, 1)) / 2, force * (sin(ang) + randrange(-1, 1)) / 2)


# Base Thing class. Can be moved, accelerated, etc. Collides with other Things.
class Thing:
    def __init__(self, x, y, sprites, unforceable=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.unforceable = unforceable
        self.spritelist = [sprite.convert_alpha() for sprite in sprites]
        self.set_sprite(0)
        self.id = len(things)
        obstacles.append(self.hitbox)
        things.append(self)
        
    def set_sprite(self, which):
        self.spriteno = which
        self.sprite = self.spritelist[which]
        self.crossarea = pi * ((self.sprite.get_width() + self.sprite.get_height()) / 2) ** 2
        self.hitbox = generatehitbox(self.x, self.y, self.sprite)  # TODO: fix hitboxes for non-square rotating Things
    
    def jerk(self, incx, incy):
        if not self.unforceable:
            self.ax += incx
            self.ay += incy
    
    def accelerate(self, incx, incy):
        self.vx += incx
        self.vy += incy
    
    def move(self, incx, incy):
        newx = self.x + incx
        newy = self.y + incy
        newhitbox = generatehitbox(newx, newy, self.sprite)
        # Assumes 1 collision...
        collision = newhitbox.collidelist(obstacles[:self.id] + obstacles[self.id + 1:])
        if collision == -1:
            qrint(newx, newy)
            self.x = newx
            self.y = newy
            self.hitbox.centerx, self.hitbox.centery = newx, newy # DON'T FORGET TO UPDATE THE HITBOX!
        else:
            qrint(collision)
            otherhit = (obstacles[:self.id] + obstacles[self.id + 1:])[collision]
            dvx, dvy = self.collide(collision, otherhit)
            other = (things[:self.id] + things[self.id + 1:])[collision]
            other.jerk(dvx, dvy)
        if debugmode:
            screen.fill((255, 0, 255), self.hitbox)
                
    def collide(self, collision, space):
        qrint(self.hitbox)
        left = (self.hitbox.centerx < space.left) - (self.hitbox.centerx > space.right)  # -1 for right, 1 for left
        up = (self.hitbox.centery < space.top) - (self.hitbox.centery > space.bottom)  # -1 for down, 1 for up
        qrint(collision, left, up,
              "\n({} - {} - {})".format(space.left, self.hitbox.centerx, space.right),
              "\n({} - {} - {})".format(space.top, self.hitbox.centery, space.bottom))
        dvx, dvy = -self.vx, -self.vy
        # if the relevant velocity component points into the object, reverse and reduce it
        if left == copysign(1, self.vx):
            self.vx *= -0.7
        if up == copysign(1, self.vy):
            self.vy *= -0.7
        dvx += self.vx
        dvy += self.vy
        return -dvx/2, -dvy/2
    
    def show(self, cycles):
        if cycles % len(self.spritelist) != self.spriteno:
            self.set_sprite(cycles % len(self.spritelist))
        self.accelerate(self.ax, self.ay)
        self.move(self.vx, self.vy)
        rotsprite = pygame.transform.rotate(self.sprite, -90 - degrees(atan2(self.vy, self.vx)))
        # used to change sprite colour to reflect speed (Blue to Red = Low to High)
        val = constrain(10 * pythag(self.vx, self.vy), 0, 255)
        pygame.PixelArray(rotsprite).replace((255, 255, 255), (val, 0, 255 - val), 0.5, (1, 1, 1))
        screen.blit(rotsprite, (self.x - rotsprite.get_width()/2, self.y - rotsprite.get_height()/2))
        self.ax = 0
        self.ay = 0


# Player class, derived from above Thing class TODO: fix craziness observed in sprite rotation whilst sitting still
class Player(Thing):
    def __init__(self, x, y, sprite, controls=(K_w, K_a, K_s, K_d), isplaying=True):
        self.controls = controls  # Input as WASD
        self.isplaying = isplaying
        super(Player, self).__init__(x, y, [sprite], False)
        players.append(self)
    
    def playerinput(self, pressed):
        if self.isplaying:
            if pressed[self.controls[0]]:
                self.jerk(0, -kickamt)
            if pressed[self.controls[1]]:
                self.jerk(-kickamt, 0)
            if pressed[self.controls[2]]:
                self.jerk(0, kickamt)
            if pressed[self.controls[3]]:
                self.jerk(kickamt, 0)
        else:
            self.jerk(*AI(player1.hitbox.center, goal1.center, squareball.hitbox.center, kickamt, player1col))
            
    def applyairresistance(self, rho=1.1839, cd=0.47):
        # F_d = (rho.v^2.A.C_d)/2
        # rho_air = 1.1839
        # C_d_sphere = 0.47
        v = pythag(self.vx, self.vy)
        if v != 0:
            a = pythag(self.ax, self.ay)
            res = -min((rho * (v**2) * self.crossarea * cd)/2000000, v - a) # Add some extra zeros...
            self.jerk((self.vx/v) * res, (self.vy/v) * res)
            
    def show(self, cycles):
        self.applyairresistance()
        super(Player, self).show(cycles)
          

# Wall class, for environment obstacles, derived from above Thing class
class Wall(Thing):
    def __init__(self, rectin, col=(255, 0, 255)):
        sprite = pygame.Surface((rectin.w, rectin.h)).convert_alpha()
        sprite.fill(col)
        super(Wall, self).__init__(rectin.x + rectin.w/2, rectin.y + rectin.h/2, [sprite], True)
    
    def set_sprite(self, which):
        self.spriteno = which
        self.sprite = self.spritelist[which]
        self.hitbox = generatehitbox(self.x, self.y, self.sprite)
    
    def collide(self, collision, space):
        return self.vx, self.vy
    
    def move(self, incx, incy):
        # Walls are moved, then back-calculate their velocity TODO: acceleration calculation?
        self.vx, self.vy = incx, incy
        super(Wall, self).move(incx, incy)
    
    def show(self, cycles):
        screen.blit(self.sprite, (self.x - self.sprite.get_width()/2, self.y - self.sprite.get_height()/2))
        self.ax = 0
        self.ay = 0

# Add in walls
screenwalls = [Wall(wallrect) for wallrect in [Rect(0, -wallthickness, w, wallthickness),
                                               Rect(-wallthickness, 0, wallthickness, h),
                                               Rect(0, h - wallthickness*3, w, wallthickness*4),
                                               Rect(w, 0, wallthickness, h)]]
upperplatform = Wall(Rect(w/2 - w/6, h/2 - 150, w/3, 50))
lowerplatform = Wall(Rect(w/2 - w/6, h/2 - 50, w/3, 50))

# basic player settings
player1col = (0, 150, 0)
player2col = (200, 0, 0)
playersprite = pygame.transform.scale(pygame.image.load_extended(r"PunchBall/FIST2.png"), (36, 36)).convert_alpha()
player1playing = True
player2playing = True

player1sprite = playersprite.copy()
pygame.draw.circle(player1sprite, player1col, (18, 24), 4)
player1 = Player(w * 0.75, h/2, player1sprite, (K_UP, K_LEFT, K_DOWN, K_RIGHT), player1playing)

player2sprite = pygame.transform.flip(playersprite, True, False)
pygame.draw.circle(player2sprite, player2col, (18, 24), 4)
player2 = Player(w * 0.25, h/2, player2sprite, isplaying=player2playing)

# Settings for the ball
ballsprite = pygame.Surface((36, 36)).convert_alpha()
ballsprite.fill((0, 0, 0, 0))
pygame.draw.circle(ballsprite, (255, 255, 255), (18, 18), 18)
pygame.draw.circle(ballsprite, (0, 0, 0, 0), (18, 24), 4)
squareball = Thing(w/2, h/10, [ballsprite])

if False:
    fishsprite = pygame.transform.scale(pygame.image.load_extended(r"PunchBall/FISH.png"), (21, 36)).convert_alpha()
    for i, fishx in enumerate(range(0, w, 36)):
        print(i, "FISH")
        Player(fishx + 18, h/1.3 + 10 * sin(radians(fishx)), fishsprite, isplaying=False)
    print("FISHPARTY!")

# Set goal positions
goal1 = Rect(0, 0, 50, 50)
goal2 = Rect(w - 50, 0, 50, 50)

# Initialise values used for keeping track of game
kickamt = 0.5
pts = 0
ingoal = 0
cycles = 0

# main game loop
while True:
    screen.fill(0)  # Clears screen
    
    # Draw goals
    screen.fill(player1col, goal1)
    screen.fill(player2col, goal2)
    
    # Move moving platforms
    upperplatform.move(5 * cos(radians(cycles)), 0)
    lowerplatform.move(-5 * cos(radians(cycles)), 0)
    
    # Obtain playerinputs
    pressed = pygame.key.get_pressed()
    
    for p in players:
        p.jerk(0, kickamt / 2.5)  # APPLY GRAVITY (only applies to players)
        p.playerinput(pressed)  # MOVEMENT (set to AI if player not playing)
        #player2.jerk(*AI(player2.hitbox.center, goal2.center, squareball.hitbox.center, kickamt, player2col))
    
    # Draw the obstacles
    for i, o in enumerate(obstacles):
        if things[i] == 0:
            screen.fill((255, 0, 255), o.clip(screenrect))  # Must clip to screen or odd constraining behaviour occurs
    
    # Point scoring mechanism
    goalhit = squareball.hitbox.collidelist([goal1, goal2])
    if goalhit == -1:
        ingoal = 0
    elif not ingoal:
        ingoal = [-1, 1][goalhit]
        pts += ingoal
        qrint(pts)
    
    # Activate and show all the Things in random order
    renderorder = things.copy()
    shuffle(renderorder)
    for t in renderorder:
        t.show(cycles)

    # Points display
    pygame.draw.rect(screen, (200, 200, 200), (w / 2 - 200, h - wallthickness * 2, 400, wallthickness))
    if pts < 0:
        pygame.draw.rect(screen, player1col, (w / 2, h - wallthickness * 2, pts * 40, wallthickness))
    elif pts > 0:
        pygame.draw.rect(screen, player2col, (w / 2, h - wallthickness * 2, pts * 40, wallthickness))
    for i in range(-200, 201, 40):
        pygame.draw.line(screen, (0, 0, 0), (w / 2 + i, h - wallthickness * 2), (w / 2 + i, h - wallthickness), 2)
    pygame.draw.line(screen, (0, 0, 0), (w / 2, h - wallthickness * 2.5), (w / 2, h - wallthickness * 0.5), 2)
            
    # Display, handle events, then pause between cycles for reasonable framerate
    pygame.display.flip()
    cycles += 1
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    sleep(0.01)
    
    # Win conditions (quits on victory)
    if pts == -5:
        print("TEAM 1 WINS")
        quit(1)
    if pts == 5:
        print("TEAM 2 WINS")
        quit(2)
