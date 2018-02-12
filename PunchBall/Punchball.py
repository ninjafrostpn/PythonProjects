import pygame, time
from pygame.locals import *
from math import atan2, degrees, copysign, pi, sin, cos
from random import shuffle, randrange

screen = pygame.display.set_mode((1000, 500))
w = screen.get_width()
h = screen.get_height()
screenrect = screen.get_rect()

wallthickness = 10
obstacles = [Rect(0,-wallthickness,w,wallthickness), Rect(-wallthickness,0,wallthickness,h),
             Rect(0,h - wallthickness*3,w,wallthickness*4), Rect(w,0,wallthickness,h),
             Rect(w/2 - w/6, h/2 - 50, w/3, 50), Rect(w/2 - w/6, h/2 - 150, w/3, 50)]

things = [0 for i in obstacles]

def constrain(val, lo, hi):
    return min(max(val, lo), hi)

def pythag(a, b):
    # if a + b > 0:
    #     print(a, b)
    return ((a ** 2) + (b ** 2)) ** 0.5

def generatehitbox(x, y, sprite, scaledoffset=0.5):
    sx = sprite.get_width()
    sy = sprite.get_height()
    #print(x - (sx * scaledoffset), y - (sy * scaledoffset), sx, sy)
    return Rect(x - (sx * scaledoffset), y - (sy * scaledoffset), sx, sy)

class Thing:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.spritelist = [sprite.convert_alpha() for sprite in sprites]
        self.set_sprite(0)
        self.id = len(things)
        # print(self.id)
        obstacles.append(self.hitbox)
        things.append(self)
        
    def set_sprite(self, which):
        self.spriteno = which
        self.sprite = self.spritelist[which]
        self.crossarea = pi * ((self.sprite.get_width() + self.sprite.get_height()) / 2) ** 2
        self.hitbox = generatehitbox(self.x, self.y, self.sprite)
    
    def __add__(self, other):
        pass
    
    def jerk(self, incx, incy):
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
            #print(newx, newy)
            self.x = newx
            self.y = newy
            # DON'T FORGET TO UPDATE THE HITBOX!
            self.hitbox.centerx, self.hitbox.centery = newx, newy
        else:
            # print(collision)
            otherhit = (obstacles[:self.id] + obstacles[self.id + 1:])[collision]
            dvx, dvy = self.collide(collision, otherhit)
            other = (things[:self.id] + things[self.id + 1:])[collision]
            if other != 0:
                other.jerk(-dvx/2, -dvy/2)
                
    def collide(self, collision, space):
        # print(self.hitbox)
        left = (self.hitbox.centerx < space.left) - (self.hitbox.centerx > space.right)  # -1 for right, 1 for left
        up = (self.hitbox.centery < space.top) - (self.hitbox.centery > space.bottom)  # -1 for down, 1 for up
        # print(collision, left, up,
        #       "\n({} - {} - {})".format(space.left, self.hitbox.centerx, space.right),
        #       "\n({} - {} - {})".format(space.top, self.hitbox.centery, space.bottom))
        dvx, dvy = -self.vx, -self.vy
        # if the velocity points into the wall
        if left == copysign(1, self.vx):
            self.vx *= -0.7
        if up == copysign(1, self.vy):
            self.vy *= -0.7
        dvx += self.vx
        dvy += self.vy
        return dvx, dvy

    def applyairresistance(self, rho=1.1839, cd=0.47):
        # F_d = (rho.v^2.A.C_d)/2
        # rho_air = 1.1839
        # C_d_sphere = 0.47
        v = pythag(self.vx, self.vy)
        if v != 0:
            a = pythag(self.ax, self.ay)
            res = -min((rho * (v**2) * self.crossarea * cd)/2000000, a) # Add some extra zeros...(and a should be v - a)
            self.jerk((self.vx/v) * res, (self.vy/v) * res)
    
    def show(self, cycles):
        if cycles % len(self.spritelist) != self.spriteno:
            self.spriteno = cycles
            self.sprite = self.spritelist[self.spriteno]
        self.applyairresistance()
        self.accelerate(self.ax, self.ay)
        self.move(self.vx, self.vy)
        rotsprite = pygame.transform.rotate(self.sprite, -90 - degrees(atan2(self.vy, self.vx)))
        # used to change sprite colour to reflect speed (Blue to Red = Low to High)
        val = constrain(10 * pythag(self.vx, self.vy), 0, 255)
        pygame.PixelArray(rotsprite).replace((255, 255, 255), (val, 0, 255 - val), 0.5, (1, 1, 1))
        screen.blit(rotsprite, (self.x - rotsprite.get_width()/2, self.y - rotsprite.get_height()/2))
        self.ax = 0
        self.ay = 0


player1col = (0, 150, 0)
player2col = (200, 0, 0)
playersprite = pygame.transform.scale(pygame.image.load_extended(r"D:\Users\Charles Turvey\Documents\Python\FIST2.png"),
                                      (36, 36)).convert_alpha()

player1sprite = playersprite.copy()
pygame.draw.circle(player1sprite, player1col, (18, 24), 4)
player1 = Thing(w * 0.75, h/2, [player1sprite])

player2sprite = pygame.transform.flip(playersprite, True, False)
pygame.draw.circle(player2sprite, player2col, (18, 24), 4)
player2 = Thing(w * 0.25, h/2, [player2sprite])

ballsprite = pygame.Surface((36, 36)).convert_alpha()
ballsprite.fill((0, 0, 0, 0))
pygame.draw.circle(ballsprite, (255, 255, 255), (18, 18), 18)
pygame.draw.circle(ballsprite, (0, 0, 0, 0), (18, 24), 4)
squareball = Thing(w/2, h/2, [ballsprite])

kickamt = 0.5
player1playing = True
player2playing = False

goal1 = Rect(0, 0, 50, 50)
goal2 = Rect(w - 50, 0, 50, 50)
pts = 0
ingoal = 0
cycles = 0
while True:
    screen.fill(0)
    screen.fill(player1col, goal1)
    screen.fill(player2col, goal2)
    obstacles[4].centerx = (1 + cos(cycles/700)) * (w/2)
    obstacles[5].centerx = (1 - cos(cycles/700)) * (w/2)
    pressed = pygame.key.get_pressed()
    # GRAVITY (only applies to players)
    player1.jerk(0, kickamt/2.5)
    player2.jerk(0, kickamt/2.5)
    # MOVEMENT (can be set to AI)
    if player1playing:
        if pressed[K_LEFT]:
            player1.jerk(-kickamt, 0)
        if pressed[K_RIGHT]:
            player1.jerk(kickamt, 0)
        if pressed[K_UP]:
            player1.jerk(0, -kickamt)
        if pressed[K_DOWN]:
            player1.jerk(0, kickamt)
    else:
        dx = goal1.centerx - squareball.x
        dy = goal1.centery - squareball.y
        d = pythag(dx, dy)
        targx = squareball.x - (20 * (dx / d))
        targy = squareball.y - (20 * (dy / d))
        #pygame.draw.circle(screen, player1col, (int(targx), int(targy)), 10)
        ang = atan2(targy - player1.y, targx - player1.x)
        player1.jerk(kickamt * (cos(ang) + randrange(-1, 1)) / 2, kickamt * (sin(ang) + randrange(-1, 1)) / 2)
    if player2playing:
        if pressed[K_a]:
            player2.jerk(-kickamt, 0)
        if pressed[K_d]:
            player2.jerk(kickamt, 0)
        if pressed[K_w]:
            player2.jerk(0, -kickamt)
        if pressed[K_s]:
            player2.jerk(0, kickamt)
    else:
        dx = goal2.centerx - squareball.x
        dy = goal2.centery - squareball.y
        d = pythag(dx, dy)
        targx = squareball.x - (20 * (dx/d))
        targy = squareball.y - (20 * (dy/d))
        #pygame.draw.circle(screen, player2col, (int(targx), int(targy)), 10)
        ang = atan2(targy - player2.y, targx - player2.x)
        player2.jerk(kickamt * (cos(ang) + randrange(-1, 1))/2, kickamt * (sin(ang) + randrange(-1, 1))/2)
    for i, o in enumerate(obstacles):
        if things[i] == 0:
            screen.fill((255, 0, 255), o.clip(screenrect)) # Must clip to screen or odd constraining behaviour occurs
    goalhit = squareball.hitbox.collidelist([goal1, goal2])
    if goalhit == -1:
        ingoal = 0
    elif not ingoal:
        ingoal = [-1, 1][goalhit]
        pts += ingoal
        print(pts)
    pygame.draw.rect(screen, (200, 200, 200), (w/2 - 200, h - wallthickness * 2, 400, wallthickness))
    if pts < 0:
        pygame.draw.rect(screen, player1col, (w/2, h - wallthickness * 2, pts * 40, wallthickness))
    elif pts > 0:
        pygame.draw.rect(screen, player2col, (w/2, h - wallthickness * 2, pts * 40, wallthickness))
    for i in range(-200, 201, 40):
        pygame.draw.line(screen, (0, 0, 0), (w/2 + i, h - wallthickness * 2), (w/2 + i, h - wallthickness), 2)
    pygame.draw.line(screen, (0, 0, 0), (w / 2, h - wallthickness * 2.5), (w / 2, h - wallthickness * 0.5), 2)
    renderorder = things.copy()
    shuffle(renderorder)
    for t in renderorder:
        if t != 0:
            t.show(cycles)
    pygame.display.flip()
    cycles += 1
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
    time.sleep(0.01)
    if pts == -5:
        print("PLAYER 1 WINS")
        quit()
    if pts ==5:
        print("PLAYER 2 WINS")
        quit()
