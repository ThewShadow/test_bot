import requests
import socket
sock = socket.socket()

if __name__ == '__main__':
    sock.connect(('127.0.0.1', 65432))
    sock.sendall(b'            23.3334242, -32.3234433               ')
    sock.close()