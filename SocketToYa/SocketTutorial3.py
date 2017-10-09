# Threaded portscanner

import socket, threading
from queue import Queue

print_lock = threading.Lock()

server = "192.168.0.12"
home = "127.0.0.1"

def pscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((home, port))
        with print_lock:
            print("Port", port, "be ready!")
    except:
        pass

def threader():
    while True:
        worker = q.get()  # workers double as port numbers
        pscan(worker)
        q.task_done()

q = Queue()

# makes workers
for i in range(700):  # how many workers available
    t = threading.Thread(target=threader)  # put workers to work
    t.daemon = True
    t.start()

# makes jobs
for worker in range(1, 10000):
    q.put(worker)  # put worker to work... add a number to the queue

q.join()
print("Complete!")
