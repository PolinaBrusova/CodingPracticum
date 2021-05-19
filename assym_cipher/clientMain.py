import socket
from client import Client

# Протокол Диффи-Хеллмана
a = 100
g = 104
p = 78

host = ''
sock = socket.socket()
sock.setblocking(1)
sock.connect((host, 7070))
print("Соединен успешно")

client = Client()
client.set_sock(sock)

try:
    with open("kclient.txt", "r") as file:
        for line in file:
            keyFullSer = int(line)
        try:
            chr(keyFullSer)
        except:
            keyFullSer = client.generate(a, g)
except:
    keyFullSer = client.generate(a, g)

port = client.mess(sock, keyFullSer)
sock.close()
sock = socket.socket()
sock.connect((host, 1024))

while True:
    client.mess(sock, keyFullSer)