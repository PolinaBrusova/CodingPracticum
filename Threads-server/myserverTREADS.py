import socket, threading

conect_user = []  # список подключенных к чату


def accept():
    # Функция регистрации и подключения клиента
    while True:
        cli_sock, cli_add = ser_sock.accept()
        conect_user.append(cli_sock)  # добавляем клиента в наш список

        # создаем новый поток для этого клиента
        thread_client = threading.Thread(target=broadcast, args=[cli_sock])

        thread_client.start()  # запускаем новый поток


def broadcast(cli_sock):
    # Функция ответа клиенту
    while True:
        try:
            data = cli_sock.recv(1024)  # запрос
            message = data.decode(encoding="utf-8")[data.decode(encoding="utf-8").find('>')+1:]
            if data:
                if message == 'exit':
                    conect_user.pop(conect_user.index(cli_sock))
                    for client in conect_user:
                        line = " server>Кто-то больше не в чате("
                        client.send(bytes(line, encoding="utf-8"))
                    cli_sock.send(bytes("over", encoding="utf-8"))

                else:
                    for client in conect_user:
                        # и отправляем сообщение всем, кроме отправителя
                        if client != cli_sock:
                            client.send(data)
        except Exception as x:
            print(x.message)
            break


# устанавливаем сокет (SOCK_STREAM - протокол, по которому cоединение устанавливается,
# и обе стороны ведут разговор до тех пор, пока соединение не будет прервано одной
# из сторон или из-за сетевой ошибки.)
ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'  # хост
port = 4040  # дефолтный порт
ser_sock.bind((host, port))

ser_sock.listen(1)  # начинаем прослушивание дефолтного порта
print('Чат начат на порте : ' + str(port))

# Создаем новый поток и запускаем его
thread_ac = threading.Thread(target=accept)
thread_ac.start()
