import pygame, threading
from pygame.locals import *
from queue import Queue
from random import shuffle

print_lock = threading.Lock()

pygame.init()

pokepath = "D:\\Users\\Charles Turvey\\Pictures\\DP Maps\\"

town = pygame.image.load_extended(pokepath + "999temp.png")
w = town.get_width()
h = town.get_height()
screen = pygame.display.set_mode((w, h))
town = town.convert_alpha()

target = pygame.image.load_extended(pokepath + "999.png").convert_alpha()

def checkfit(areaw, areah, arear, areag, areab,
             itemw, itemh, itemr, itemg, itemb, itema,
             posx, posy, threshold=10, sample=10):
    totscore = 0
    # Check for compatibility
    coords = [(i, j) for i in range(itemw) for j in range(itemh)]
    shuffle(coords)
    counter = 0
    while len(coords) > 0:
        i, j = coords.pop()
        counter += 1
        if i < 0 or i >= areaw or j < 0 or j >= areah:
            totscore += 127
        else:
            if itema[i][j] == 0:
                pass
            else:
                rscore = abs(int(arear[i + posx][j + posy]) - int(itemr[i][j]))
                gscore = abs(int(areag[i + posx][j + posy]) - int(itemg[i][j]))
                bscore = abs(int(areab[i + posx][j + posy]) - int(itemb[i][j]))
                totscore += (rscore + gscore + bscore)/3.0
        if counter % sample == 0:
            if (totscore / counter) > threshold:
                return False
    return (totscore / counter) < threshold



def scan(area, item, xborder=0, yborder=0):
    areaw = area.get_width()
    areah = area.get_height()
    itemw = item.get_width()
    itemh = item.get_height()
    # print(areaw, areah, itemw, itemh)
    
    # 2D pixel arrays of the RGB of the search area
    arear = pygame.surfarray.pixels_red(area)
    areag = pygame.surfarray.pixels_green(area)
    areab = pygame.surfarray.pixels_blue(area)
    # and of the item being searched for
    itema = pygame.surfarray.pixels_alpha(item)
    itemr = pygame.surfarray.pixels_red(item)
    itemg = pygame.surfarray.pixels_green(item)
    itemb = pygame.surfarray.pixels_blue(item)

    q = Queue()
    for i in range(-xborder, areaw + xborder - itemw):
        q.put(i)
    fits = []
    
    def colthread(i):
        for j in range(-yborder, areah + yborder - itemh):
            # print(j)
            if checkfit(areaw, areah, arear, areag, areab,
                        itemw, itemh, itemr, itemg, itemb, itema,
                        i, j, 10, 10):
                fits.append((i, j))
        q.get()
        q.task_done()
    
    for i in range(-xborder, areaw + xborder - itemw):
        print(i)
        t = threading.Thread(target=colthread, args=[i])
        t.start()
        if len(fits) > 0:
            print("DONE")
            break
    #q.join()
    # print(fits)
    del itemr, itemg, itemb, itema
    return fits

pclocations = scan(town, target, -90, -400)
print("Meh")
screen.fill(255)
pygame.display.flip()
for location in pclocations:
    screen.blit(target, location)

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
