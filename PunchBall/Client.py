import socket, threading, pygame
from pygame.locals import *
from queue import Queue
from time import sleep

pygame.init()

print_lock = threading.Lock()

q = Queue()

pressed = set()

def sending():
    while True:
        data = ",".join([str(k) for k in pressed])
        s.send(str.encode(data))
        pressed.clear()
        sleep(0.01)

def receiving():
    while True:
        data = s.recv(4096)
        with print_lock:
            print(data.decode("utf-8"))

addr = ("139.166.166.21", 8080)
homeaddr = ("127.0.0.1", 9001)
piaddr = ("192.168.0.30", 9001)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

broken = True
while broken:
    try:
        s.connect(homeaddr)
        broken = False
        print("Connected up :)")
    except:
        print("Nope")
sender = threading.Thread(target=sending)
sender.start()
receiver = threading.Thread(target=receiving)
receiver.start()

screen = pygame.display.set_mode((500, 50))
screen.fill((255, 0, 0))
pygame.display.flip()
while True:
    for i, k in enumerate(pygame.key.get_pressed()):
        if k:
            pressed.add(i)
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
