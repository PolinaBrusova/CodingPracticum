# сервер (пункты 1-10)
import socket
import logging
import json

# простенькая текстовая бд клиентов для идентификации

users = {}
try:
    with open("users.txt", "r") as f:
        users = json.load(f)
        print(users)
except Exception as e:
    print(e)
    users = {}


def get_logger():
    """
    Функция вывода служебных сообщений в специальный лог-файл

    """

    # создаем объект логирования, называем его server
    logger = logging.getLogger("server")

    # будет отображать логи, где все идет хорошо и без ошибок
    logger.setLevel(logging.INFO)

    # куда будем записывать логи
    file_hanlder = logging.FileHandler("server.log")

    # применяем желаемое для логирования отформатирование
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # устанавливаем данное форматирование для хэндлера
    file_hanlder.setFormatter(formatter)

    # добавляем данный хендлер к нашему объекту логирования
    logger.addHandler(file_hanlder)

    return logger


logger = get_logger()
logger.info('Сервер запущен')
sock = socket.socket()

# проверка порта, как в клиенте
while True:
    port = int(input("Введите порт: "))
    if port == "":
        port = 4040
    elif 0 < int(port) < 65535:
        break
    else:
        print("Введите порт корректно")
print(port)

# проверяем есть ли свободный порт
while port < 65535:
    if port >= 65535:
        raise AssertionError("Все порты заняты")
    try:
        print("Повторное соединение...")
        sock.bind(('', port))
        break
    except socket.error:
        # пытаемся подключиться к следующему порту
        port += 1

# добавляем в логгер запись о том, что мы нашли свободный порт и прослушиваем его
logger.info(f'Начало прослушивание порта {str(port)}')
sock.listen(1)

passwd = 0  # переменная для мониторинг правильности введенного пароля
client = 1  # подключен клиент или нет

# цикл работы сервера с клиентом
while True:
    try:
        if client == 1:
            conn, addr = sock.accept()  # получаем соединение и IP-адрес подключения
            user_port = addr[1]
            data = conn.recv(1024).decode()
            user = data[data.find(' ')+1:]
            if user in users.keys():
                conn.send(str(user_port).encode() + ". Введите пароль:".encode())
            else:
                conn.send("Придумайте пароль:".encode())
            logger.info('Клиент ' + str(user) + ' подключен')  # логируем запись о подключении клиента
            client = 0

        else:
            data = conn.recv(1024).decode()
            password = data[data.find(" ")+1:]
            if not data:
                # если не пришли данные от клиента
                logger.info("Отключение клиента...")  # логируем его отключение
                client = 1
                passwd = 0
            elif passwd == 0:  # Если мы еще не ввели пароль или ввели его неверно
                if user in users.keys():
                    # для пользователя, кто сейчас подключен проверяем что data - пароль
                    if password == users[user]:
                        conn.send("Пароль введен верно".encode())
                        passwd = 1
                    else:
                        passwd = 0
                        conn.send("Пароль введен неверно. Введите верный пароль:".encode())
                else:
                    # если подключенного пользователя не нашлось в нашей бд то
                    passwd = 1  # автоматически разрешаем ему войти после авторизации
                    users[user] = password  # устанавливаем ему пароль и заносим в бд
                    print("Новый пользователь")

                    conn.send("Пользователь зарегистрирован".encode())

            else:
                # в других случаях просто обрабатываем введенные данные
                # так же логируем все происходящее
                print("Данные получены: " + data[8::])
                logger.info("Данные получены:")
                if data[8::] != "exit":
                    conn.send(data[8::].upper().encode())
                    logger.info("Отправка данных клиенту...")
                else:
                    try:
                        with open("users.txt", "w") as f:
                            json.dump(users, f)
                    except:
                        pass


    except ConnectionResetError:
        break

# закрываем соединение
conn.close()
print("Закрыли соединение")
print(users)

# пополняем бд аутентификации после окончания работы
try:
    with open("users.txt", "w") as f:
        json.dump(users, f)
except:
    pass

# логируем остановку работы сервера и закрываем сокет
logger.info("Сервер остановлен")
sock.close()
