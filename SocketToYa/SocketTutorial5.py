import socket
from _thread import *
import threading

print_lock = threading.Lock()

host = ''  # accept anything
port = 9001  # socket with the minimally maximal power level
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)  # size of queue of how many connections accepted
print("Awaiting contact...")

def threaded_client(conn, no):
    conn.send(str.encode("Hey there, Client " + str(no)))
    while True:
        data = conn.recv(4096)
        reply = "Received from Client " + str(no) + ": " + data.decode('utf-8')
        with print_lock:
            print(reply)
        if not data:
            break
        conn.sendall(str.encode(reply))
    conn.close()

connno = 0
while True:
    conn, addr = s.accept()
    with print_lock:
        print("Connected to " + str(addr[0]) + ":" + str(addr[1]) + ", Client " + str(connno))
    start_new_thread(threaded_client, (conn, connno))
    connno += 1
