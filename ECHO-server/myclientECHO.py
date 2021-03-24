from socket import *

sock = socket(SOCK_DGRAM)  # устанавливаем сокет (SOCK_DGRAM - протокол, по которому на один запрос приходит один ответ)

while True:
    # проверка порта
    port = input("Введите порт: ")
    if port == "":
        port = 4040
    elif port.isdigit() and 0 < int(port) < 65535:
        break
    else:
        print("Введите порт корректно")

# аналогично порту
while True:
    host = input("Введите хост: ")
    if host == "":
        host = "localhost"
    try:
        print(host, port)
        sock.connect((host, int(port)))
        break
    except gaierror:
        print("Не удалось подключиться")

while True:
    promt = input("Введите данные: ")

    if promt == "exit":
        sock.send("Клиент: ".encode() + promt.encode())
        break
    # отправляем серверу сообщение с дополнением фиксированной длинны
    sock.send("Клиент: ".encode() + promt.encode())
    data = sock.recv(1024)
    if data:
        print("От сервера| "+data.decode())
    else:
        print("Сервер разорвал соединение")
        break

print("Соединение прервано")
sock.close()
