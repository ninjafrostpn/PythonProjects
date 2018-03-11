import socket
import threading
import pygame
from pygame.locals import *
from time import sleep
import numpy as np

pygame.init()

print_lock = threading.Lock()
pos_lock = threading.Lock()

pressed = set()
prevpressed = set()


def sending():
    try:
        while running and not connecting:
            # only sends data if something has changed
            if prevpressed != pressed:
                #print(prevpressed, pressed)
                data = ",".join([str(k) for k in pressed] + ["-1,"])
                s.send(str.encode(data))
                prevpressed.clear()
                prevpressed.update(pressed)
            sleep(0.01)  # otherwise it doesn't send things
    except Exception as e:
        with print_lock:
            print("Sending error:", e)
    with print_lock:
        print("Finished sending")


def receiving():
    try:
        rawdata = bytes()
        while running and not connecting:
            try:
                rawdata += s.recv(4096)
            except socket.timeout:  # timeout so that the game can actually disconnect/reconnect
                pass
            infostart = rawdata.find(b'(') + 1
            infoend = rawdata.find(b')')
            # print("INFO:", infostart, infoend, rawdata[infostart: infoend])
            if infostart > 0 and infoend > -1:
                spritestart = rawdata.find(b'{{', infoend + 1) + 2
                spriteend = rawdata.find(b'}}', infoend + 1)
                # print("SPRITE:", spritestart, spriteend, len(rawdata[spritestart: spriteend]))
                if spritestart > 1 and spriteend > -1:
                    idstart = rawdata.find(b'[', spriteend + 2) + 1
                    idend = rawdata.find(b']', spriteend + 2)
                    # print("ID:", idstart, idend, rawdata[idstart: idend])
                    if idstart > 0 and idend > -1:
                        spritew, spriteh = [int(i) for i in rawdata[infostart: infoend].decode('utf-8').split(",")]
                        spritedata = rawdata[spritestart: spriteend]
                        sprite = pygame.Surface((spritew, spriteh)).convert_alpha()
                        ps = np.frombuffer(spritedata, dtype=np.uint8).reshape(spritew, spriteh, 3)
                        pygame.pixelcopy.array_to_surface(sprite, ps)
                        spriteid = int(rawdata[idstart: idend].decode('utf-8'))
                        with pos_lock:
                            sprites[spriteid] = sprite
                            spritexs[spriteid] = 0
                            spriteys[spriteid] = 0
                            spriteangs[spriteid] = 0
                        # print("{} is {} x {}".format(spriteid, spritew, spriteh))
                        rawdata = rawdata[idend + 1:]
                else:
                    if rawdata[rawdata.find(b'+') + 1:].find(b'+') > -1:
                        pass
                    posmarker = rawdata.find(b'~', infoend + 1)
                    idstart = rawdata.find(b'[', infoend + 1) + 1
                    idend = rawdata.find(b']', infoend + 1)
                    # print("ID:", idstart, idend, rawdata[idstart: idend])
                    if posmarker > -1 and idstart > 0 and idend > -1:
                        spritex, spritey, spriteang = [float(i) for i in rawdata[infostart: infoend].decode('utf-8').split(",")]
                        spriteid = int(rawdata[idstart: idend].decode('utf-8'))
                        rotsprite = pygame.transform.rotate(sprites[spriteid], -90 - spriteang).convert_alpha()
                        screen.blit(rotsprite, (spritex, spritey))
                        # with pos_lock:
                        #     spritexs[spriteid] = spritex
                        #     spriteys[spriteid] = spritey
                        #     spriteangs[spriteid] = spriteang
                        # print("{}: ({}, {}, {})".format(spriteid, spritex, spritey, spriteang))
                        rawdata = rawdata[idend + 1:]
    except Exception as e:
        with print_lock:
            print("Receiving error:", e)
    with print_lock:
        print("Finished receiving")


addr = ("139.166.166.21", 8080)
homeaddr = ("127.0.0.1", 9001)
piaddr = ("192.168.0.30", 9001)

screen = pygame.display.set_mode((1000, 500))
connecting = True
running = True
sender = 0
receiver = 0
sprites = dict()
spritexs = dict()
spriteys = dict()
spriteangs = dict()
while running:
    if connecting:
        try:
            s.close()
        except NameError:
            print("Let's get this party started...")
        except Exception as e:
            print("Couldn't disconnect:", e)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broken = True
        while broken:
            try:
                s.connect(homeaddr)
                # Adds a socket timeout, so that if recv or send do not block game exit too long
                s.settimeout(2)
                broken = False
                print("Connected up :)")
            except Exception as e:
                print("Failed to connect:", e)
            sleep(1)
        connecting = False
        print("Starting sending")
        sender = threading.Thread(target=sending)
        sender.start()
        print("Starting receiving")
        receiver = threading.Thread(target=receiving)
        receiver.start()
    #screen.fill(0)
    # with pos_lock:
    #     for i in sprites.keys():
    #         rotsprite = pygame.transform.rotate(sprites[i], -90 - spriteangs[i])
    #         screen.blit(rotsprite, (spritexs[i], spriteys[i]))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            pressed.add(e.key)
            if e.key == K_ESCAPE:
                running = False
        elif e.type == KEYUP:
            pressed.remove(e.key)
    connecting = (threading.active_count() != 3)
