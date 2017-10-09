# pretend browser

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(s)

server = 'pythonprogramming.net'
server_ip = socket.gethostbyname(server)
port = 80  # access like a browser

request = "GET / HTTP/1.1\nHost:" + server + "\n\n"

s.connect((server, port))
s.send(request.encode())  # must encode string as bytestring
result = s.recv(4096)     # buffering
while len(result) > 0:
    print(result)
    result = s.recv(4096)
