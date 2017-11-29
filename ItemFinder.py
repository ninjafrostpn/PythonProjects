import pygame, threading
from pygame.locals import *
from queue import Queue

print_lock = threading.Lock()

pygame.init()

pokepath = "D:\\Users\\Charles Turvey\\Pictures\\DP Maps\\"

town = pygame.image.load_extended(pokepath + "FaceGraph.png")
w = town.get_width()
h = town.get_height()
screen = pygame.display.set_mode((w, h))
town.convert()

target = pygame.image.load_extended(pokepath + "SamFace.png")
target.convert()

def checkfit(area, item, pos, threshold=10):
    areaw = area.get_width()
    areah = area.get_height()
    itemw = item.get_width()
    itemh = item.get_height()
    totscore = 0
    #print(areaw, areah, itemw, itemh)
    # 2D pixel arrays of the RGB of the search area
    arear = pygame.surfarray.pixels_red(area)
    areag = pygame.surfarray.pixels_green(area)
    areab = pygame.surfarray.pixels_blue(area)
    # and of the item being searched for
    itema = pygame.surfarray.pixels_alpha(item)
    itemr = pygame.surfarray.pixels_red(item)
    itemg = pygame.surfarray.pixels_green(item)
    itemb = pygame.surfarray.pixels_blue(item)
    # Check for compatibility
    for i in range(itemw):
        if i < 0 or i >= areaw:
            totscore += 127
        else:
            for j in range(itemh):
                if j < 0 or j >= areah:
                    totscore += 127
                else:
                    if itema[i][j] == 0:
                        totscore += 0
                    else:
                        rscore = abs(int(arear[i + pos[0]][j + pos[1]]) - int(itemr[i][j]))
                        gscore = abs(int(areag[i + pos[0]][j + pos[1]]) - int(itemg[i][j]))
                        bscore = abs(int(areab[i + pos[0]][j + pos[1]]) - int(itemb[i][j]))
                        totscore += (rscore + gscore + bscore)/3.0
    return (totscore / (itemw * itemh)) < threshold



def scan(area, item, xborder=0, yborder=0):
    areaw = area.get_width()
    areah = area.get_height()
    itemw = item.get_width()
    itemh = item.get_height()
    # print(areaw, areah, itemw, itemh)

    q = Queue()
    for i in range(-xborder, areaw + xborder - itemw):
        q.put(i)
    fits = []
    
    def colthread(i):
        for j in range(-yborder, areah + yborder - itemh):
            if checkfit(area, item, (i, j), 5):
                fits.append((i, j))
        q.get()
        q.task_done()
    
    for i in range(-xborder, areaw + xborder - itemw):
        print(i)
        t = threading.Thread(target=colthread, args=[i])
        t.start()
    q.join()
    # print(fits)
    return fits

pclocations = scan(town, target)
screen.fill(255)
for location in pclocations:
    screen.blit(target, location)

while True:
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
