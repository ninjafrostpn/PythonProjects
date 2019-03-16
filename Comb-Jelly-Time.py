from datetime import datetime
import numpy as np
import pygame
from pygame.locals import *
import pycountry as pc
import pytz
import reverse_geocoder as rg
from time import sleep
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()

if False:
    while True:
        lat, lon = (1 - (2 * np.random.random(2))) * (90, 180)
        # print(lat, lon)
        try:
            timezoneobject = pytz.timezone(tf.timezone_at(lng=lon, lat=lat))
            timedata = datetime.now(timezoneobject)
            if timedata.hour == 10 and timedata.minute == 4:
                place = rg.get((lat, lon), mode=1, verbose=False)
                placename = [place["name"],
                             place["admin2"], place["admin1"],
                             pc.countries.get(alpha_2=place["cc"]).name]
                try:
                    placename.remove("")
                except ValueError:
                    pass
                i = 0
                while i < len(placename) - 1:
                    if placename[i].upper() == placename[i + 1].upper():
                        placename.pop(i)
                    else:
                        i += 1
                print("Comb Jelly Time in {}!!! (UTC{})\nLocal Time = 10:04, UTC = {}"
                      .format(", ".join(placename),
                              str(datetime.now(timezoneobject))[-6:],
                              str(datetime.utcnow().time())[:5]))
                sleep(65)
        except AttributeError as e:
            pass
else:

    pygame.init()

    w, h = 500, 500
    screen = pygame.display.set_mode((w, h))
    screensize = np.int32((w, h))

    for i in range(-180, 181, 5):
        for j in range(-90, 91, 5):
            try:
                timezonename = tf.timezone_at(lng=i, lat=j)
                timezoneobject = pytz.timezone(timezonename)
                timestring = datetime.now(timezoneobject)
                points = 200 + (np.float32(tf.get_geometry(timezonename, coords_as_pairs=True)[0][0]) * (1, -1))
                # print(points)
                pygame.draw.polygon(screen, np.random.randint(0, 255, 3, "int32"), points)
                # print(i, j, timezonename, timestring)
            except Exception as e:
                pass # print(i, j, e)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == QUIT:
                quit()

    keys = set()

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                quit()
            elif e.type == KEYDOWN:
                keys.add(e.key)
                if e.key == K_ESCAPE:
                    quit()
            elif e.type == KEYUP:
                keys.discard(e.key)
        sleep(0.001)
