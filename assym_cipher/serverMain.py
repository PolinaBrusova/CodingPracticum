import socket
from server import Server

# Протокол Диффи-Хеллмана
g = 120
a = 67
p = 100

server = Server()

host = ''
port = server.scanner(host)
print(port)
sock = socket.socket()
sock.bind(('', 7070))
sock.listen(3)
conn, addr = sock.accept()
print("Соединен успешно, ", addr)

try:
    with open("kserver.txt", "r") as file:
        for line in file:
            keyFullMess = int(line)
except:
    keyFullMess = server.generate(a, g)

server.new_port(conn, keyFullMess, port)
sock.close()
sock = socket.socket()
sock.bind((host, int(port)))
sock.listen(1)
conn, addr = sock.accept()

while True:
    server.mess(conn, keyFullMess)
sock.close()