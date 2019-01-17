import pygame
# import twitter
from pygame.locals import *
from io import BytesIO
import urllib.request as ur

pygame.init()

# twit = twitter.Api(consumer_key="DOB7Rr5SHg48rK8VBSTGnLoRe",
#                    consumer_secret="T7rvjDvtx6QTDIerftG8fqACxhGv3BmCCHFIJRuwzbBGY4WZYs",
#                    access_token_key="778583630184611840-Rb2vsoSn0VHxWr9TuDECr6eUsPxgrLP",
#                    access_token_secret="GYQHdi6fCFb5RaeNme2RjHf2pMblj17gCWYy7cAqEOEIY")

alotfiles = "D:\\Users\\Charles Turvey\\Pictures\\Art\\Alots\\"

alotpath = alotfiles + "Blank.png"
alot = pygame.image.load_extended(alotpath)

w = alot.get_width()
h = alot.get_height()

lft = w
rgt = 0
top = h
btm = 0
alotalpha = pygame.surfarray.array_alpha(alot)
for i in range(w):
    for j in range(h):
        if alotalpha[i][j] == 0:
            lft = min(lft, i)
            rgt = max(rgt, i)
            top = min(top, j)
            btm = max(btm, j)
framew = rgt - lft
frameh = btm - top

screen = pygame.display.set_mode((w, h))
alot.convert()

# Distilled from https://github.com/hardikvasa/google-images-download/blob/master/google-images-download.py
search = "%20".join(input(">>> ").split())
url = 'https://www.google.com/search?q=' + search + \
      '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
headers = {'User-Agent':
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
req = ur.Request(url, headers=headers)
resp = ur.urlopen(req)
respData = str(resp.read())
print(respData)
urls = []
for i in range(10):
    start_line = respData.find('"class="rg_meta"')
    start_content = respData.find('"ou"', start_line + 1)
    end_content = respData.find(',"ow"', start_content + 1)
    url = str(respData[start_content + 6: end_content - 1])
    print(url)
    urls.append(url)
    respData = respData[end_content:]


def preparealot(imageno):
    otherfile = alotpath
    while len(urls) > 1:
        try:
            otherfile = BytesIO(ur.urlopen(urls[imageno]).read())
            break
        except Exception as E:
            failedurl = urls.pop(imageno)
            imageno %= len(urls)
            print("ERROR WITH {}: {}".format(failedurl, str(E)))
    other = pygame.image.load_extended(otherfile)
    other.convert()

    imagew = other.get_width()
    imageh = other.get_height()
    scalew = framew / imagew
    scaleh = frameh / imageh
    scale = max(scalew, scaleh)
    other = pygame.transform.scale(other, (int(imagew * scale), int(imageh * scale)))
    
    screen.blit(other, (lft + int((framew - other.get_width()) / 2), top + int((frameh - other.get_height()) / 2)))
    screen.blit(alot, (0, 0))
    pygame.display.flip()
    

pointer = 0
preparealot(0)
while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            elif e.key == K_RIGHT:
                pointer = (pointer + 1) % len(urls)
                preparealot(pointer)
            elif e.key == K_LEFT:
                pointer = (pointer - 1) % len(urls)
                preparealot(pointer)
            elif e.key == K_RETURN:
                pygame.image.save(screen,
                                  alotfiles + "Autogenerated\\alot_of_{}.png".format("_".join(search.split("%20"))))
