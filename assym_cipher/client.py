from utils import assym, encode, decode
from termcolor import colored


class Client:
    sock = None

    def set_sock(self, sock):
        self.sock = sock

    def generate(self, a, g):
        message = str(a)
        self.sock.send(message.encode())
        try:
            public_k = int(self.sock.recv(1024))
        except ValueError:
            public_k = ''
            print(colored("Значение ключа неверно", "red"))
        parts1 = assym(g, a, public_k)
        message = str(parts1)
        self.sock.send(message.encode())
        parts2 = int(self.sock.recv(1024))

        key_full_m = assym(parts2, a, public_k)
        message = str(key_full_m)
        self.sock.send(message.encode())
        key_full_s = int(self.sock.recv(1024))
        with open("kclient.txt", "w") as file:
            file.write(str(key_full_s))
        return key_full_s

    @staticmethod
    def mess(sock, full_message):
        try:
            msg = input(colored('введите сообщение: ', "blue"))
            msg_new = encode(msg, full_message)
            print(colored("результат шифрования: "+msg_new, "blue"))
            sock.send(msg_new.encode())
            msg = sock.recv(1024).decode()
            msg_new = decode(msg, full_message)
            print("от сервера: ", msg_new)
        except ValueError:
            print(colored("числовое значение должно быть меньше", "red"))
