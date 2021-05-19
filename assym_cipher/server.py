import socket
from utils import assym, valid, encode, decode
from termcolor import colored


class Server:
    conn = None

    def set_conn(self, conn):
        self.conn = conn

    def generate(self, a, p):
        publicKey = int(self.conn.recv(1024))
        if valid(publicKey):
            msg = str(p)
            self.conn.send(msg.encode())
        else:
            print(colored("Значение ключа неверно", "red"))

        key_part_s = int(self.conn.recv(1024))
        key_part_m = assym(publicKey, a, p)
        msg = str(key_part_m)
        self.conn.send(msg.encode())

        key_full_s = int(self.conn.recv(1024))
        key_full_m = assym(key_part_s, a, p)
        msg = str(key_full_m)
        self.conn.send(msg.encode())
        print(key_full_s)
        with open("kserver.txt", "w") as file:
            file.write(str(key_full_m))

        return key_full_m

    @staticmethod
    def mess(conn, key_full_m):
        msg = conn.recv(1024).decode()
        msg_new = decode(msg, key_full_m)
        print("от клиента: ", msg_new)
        msg1 = input(colored("введите сообщение: ", "blue"))
        msg_new1 = encode(msg1, key_full_m)
        print(colored("результат ширфования: "+msg_new1, "blue"))
        conn.send(msg_new1.encode())
        return msg_new

    @staticmethod
    def new_port(conn, full_message, port):
        message = conn.recv(1024).decode()
        messageOfClient = decode(message, full_message)
        print("от клиента (ПОРТ): ", messageOfClient)
        messageReceived = str(port)
        print(colored("введите сообщение: "+messageReceived, "yellow"))
        messageOfServer = encode(messageReceived, full_message)
        conn.send(messageOfServer.encode())

    @staticmethod
    def scanner(host_str):
        sock = socket.socket()
        for i in range(1024, 65536):
            try:
                sock.bind((host_str, i))
                scanPort = i
                sock.close()
                return scanPort
            except socket.error:
                pass
