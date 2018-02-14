import socket
from _thread import *
import threading
import pygame
from pygame.locals import *

pygame.init()

print_lock = threading.Lock()
input_lock = threading.Lock()

host = ''  # accept anything
port = 9001  # socket with the minimally maximal power level
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)  # size of queue of how many connections accepted
print("Awaiting contact...")

pressed = set()

def threaded_client(conn, no):
    conn.send(str.encode("Hey there, Client " + str(no)))
    while True:
        data = conn.recv(4096).decode('utf-8').split(",")
        with print_lock:
            print(data)
        if not data:
            break
        for k in data:
            with input_lock:
                pressed.add(int(k))
        # with print_lock:
        #     print(pressed)
    conn.close()

screen = pygame.display.set_mode((500, 500))

clients = []
def clientfinder():
    while True:
        conn, addr = s.accept()
        connno = len(clients)
        with print_lock:
            print("Connected to " + str(addr[0]) + ":" + str(addr[1]) + ", Client " + str(connno))
        clients.append(start_new_thread(threaded_client, (conn, connno)))

start_new_thread(clientfinder, ())

def waspressed(which):
    if which in pressed:
        pressed.remove(which)
        return True
    return False

posx, posy = 0, screen.get_height()/2 - 50
while True:
    screen.fill(0)
    if waspressed(K_UP):
        posy -= 10
    if waspressed(K_LEFT):
        posx -= 10
    if waspressed(K_DOWN):
        posy += 10
    if waspressed(K_RIGHT):
        posx += 10
    screen.fill(255, (posx, posy, 100, 100))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
            if e.key == K_d:
                posx += 10
