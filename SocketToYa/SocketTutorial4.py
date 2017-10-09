import socket

host = ''  # accept anything
port = 9001  # socket with the minimally maximal power level
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)  # size of queue of how many connections accepted
conn, addr = s.accept()

print("Connected to", addr[0], ":", addr[1])

# https://www.youtube.com/watch?v=Q1a12QFq3os
