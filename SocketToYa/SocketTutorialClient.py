import socket, threading
from queue import Queue

print_lock = threading.Lock()

q = Queue()

def sending():
    while True:
        data = input()
        s.send(str.encode(data))

def receiving():
    while True:
        data = s.recv(4096)
        with print_lock:
            print(data.decode("utf-8"))

addr = ("139.166.166.21", 8080)#("127.0.0.1", 9001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

broken = True
while broken:
    try:
        s.connect(addr)
        broken = False
        print("Connected up :)")
    except:
        print("Nope")
sender = threading.Thread(target=sending)
sender.start()
receiver = threading.Thread(target=receiving)
receiver.start()
