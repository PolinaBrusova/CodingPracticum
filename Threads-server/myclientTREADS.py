import socket, threading

HOST = 'localhost'
PORT = 4040

# Вводим имя для чата
name = input('Давайте зарегистрируемся. Ваше имя?  >>> ')


# Функция отправки сообщений с определенным началом
def send(name):
    while True:
        msg = input(f'\n {name} > ')
        data = name + '>' + msg
        cli_sock.send(bytes(data, encoding="utf-8"))
        if msg == "exit":
            raise KeyboardInterrupt

# функция принятия сообщений
def receive():
    while True:
        data = cli_sock.recv(1024)
        if data.decode(encoding="utf-8")[data.decode(encoding="utf-8").find(">")+1:] == "over":
            raise KeyboardInterrupt
            break
        else:
            print('\tОТ ' + str(data.decode(encoding="utf-8")))


if __name__ == "__main__":
    # создаем сокет (SOCK_STREAM - протокол, по которому cоединение устанавливается,
    # и обе стороны ведут разговор до тех пор, пока соединение не будет прервано одной
    # из сторон или из-за сетевой ошибки.)
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    cli_sock.connect((HOST, PORT))


    # создаем новый поток и запускаем его (потоку даем имя, которое пользователь выбрал для себя для чата)
    thread_send = threading.Thread(target=send, args=[name])
    thread_send.start()


    # начинаем получать данные
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()