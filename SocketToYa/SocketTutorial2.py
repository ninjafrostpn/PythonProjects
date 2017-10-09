# slow portscanner

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = 'pythonprogramming.net'
def pscan(port):
    try:
        s.connect((server, port))
        return True
    except:
        return False

for i in range(1, 26):
    if pscan(i):
        print("Port", i, "be open for business!")
    else:
        print("Port", i, "be closed!")
