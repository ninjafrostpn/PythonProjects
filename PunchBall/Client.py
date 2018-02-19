import socket, threading, pygame
from pygame.locals import *
from time import sleep
import numpy as np

pygame.init()

print_lock = threading.Lock()

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
        while running and not connecting:
            data = bytes()
            while running and not connecting and (len(data) < 1500000):
                try:
                    data += s.recv(1500000)
                except socket.timeout:  # timeout so that the game can actually disconnect/reconnect
                    pass
            if running and not connecting:
                ps = np.frombuffer(data[:1500000], dtype=np.uint8).reshape(1000, 500, 3)
                pygame.pixelcopy.array_to_surface(screen, ps)
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
    sleep(0.01)
