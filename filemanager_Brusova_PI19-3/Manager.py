import os
import shutil


class FileManager:

    def __init__(self, home_dir, help_text):
        """
        :param home_dir: String
        :param help_text: String
        """
        self.home_dir = home_dir
        self.temp_dir = home_dir
        self.help_text = help_text

    def getCurrent(self):
        """
        Метод возвращает путь к текущей директории
        :return: String
        """
        return self.temp_dir

    @staticmethod
    def __not_path(file_name):
        """
        Метод для проверки, что строка не является путем
        :param file_name: String
        :return: Boolean
        """
        if "/" not in file_name:
            return True
        else:
            return False

    def __dir_in_root(self, path):
        """
        Метод для проверки, что строка является путем, а так же не выходит
        за пределы установленного домашнего каталога.
        :param path: String
        :return: Boolean
        """
        if "/" in path and self.home_dir in path:
            return True
        else:
            return False


    def cd(self, new_dir):
        """
        Метод смены директории
        :param new_dir: String
        """
        if len(new_dir) == 6 and new_dir[4] == new_dir[5] == ".":
            if self.temp_dir != self.home_dir:
                temp = self.temp_dir[:self.temp_dir.rfind("/")]
                os.chdir(temp)
                self.temp_dir = temp
        elif len(new_dir) > 6 and new_dir[4] == " ":
            name = new_dir.replace("goto ", "")
            try:
                temp = self.temp_dir + "/" + name
                os.chdir(temp)
                self.temp_dir = temp
            except Exception:
                print("Нет такой директории. Введите files для посмотра содержания текущей директории.")

    def create(self, command):
        """
        Метод создания директории
        :param command: String
        """
        try:
            name = command.replace("create ", "")
            os.mkdir(self.temp_dir + "/" + name)
            print("Папка успешно создана.")
        except Exception as e:
            print("Папки не существует.")

    def delete(self, command):
        """
        Метод удаления (папки и файла по названию)
        :param command: String
        """
        try:
            name = command.replace("delete ", "")
            shutil.rmtree(self.temp_dir + "/" + name)
            print("Удаление папки прошло успешно.")
        except Exception as e:
            try:
                os.remove(self.temp_dir + "/" + name)
                print("Удаление файла прошло успешно.")
            except Exception as e:
                print("Папки или файла не существует.")

    def touch(self, command):
        """
        Метод создания пустого вайла с конкретным названием
        :param command: String
        """
        try:
            name = command.replace("make ", "")
            if not name.startswith(" "):
                with open(self.temp_dir + "/" + name, "w"):
                    pass
                print("Файл успешно создан.")
            else:
                print("Недопустимое имя файла")
        except Exception as e:
            print("Папки не существует или в названии присутствуют неопустимые символы.")

    def write(self, command):
        """
        Метод записи содержимого в файл
        :param command: String
        """
        try:
            name = command.replace("write ", "")
            text = name[name.find(" ") + 1:]
            name = name[:name.find(" ")]
            with open(self.temp_dir + "/" + name, "a+") as f:
                f.write("\n" + text)
            print("Данные записаны.")
        except Exception as e:
            print("Файла не существует.")

    def read(self, command):
        """
        Метод чтения содержимого файла
        :param command: String
        """
        try:
            name = command.replace("read ", "")
            with open(self.temp_dir + "/" + name, "r") as f:
                line = f.read()
                print(line)
        except Exception as e:
            print("Файла не существует.")

    def copy(self, command):
        """
        Метод копирования указаного файла в указанную диреткторию
        :param command: String
        """
        try:
            command_body = command.replace("copy ", "")
            first_file = command_body[:command_body.find(" ")]
            command_body = command_body.replace(first_file + " ", "")
            second_file = command_body
            if self.__not_path(first_file) and self.__not_path(second_file):
                shutil.copyfile(self.temp_dir + "/" + first_file, self.temp_dir + "/" + second_file)
            else:
                if self.__dir_in_root(first_file) and self.__dir_in_root(second_file):
                    shutil.copyfile(first_file, second_file)
                else:
                    print("Данные не могут быть скопированы, директории или файлы не найдены")
        except Exception as e:
            print("Файла не существует.")

    def move(self, command):
        """Метод перемещения указаного файла или директории в указанную диреткторию
        :param command: String
        """
        try:
            command_body = command.replace("move ", "")
            first_file = command_body[:command_body.find(" ")]
            command_body = command_body.replace(first_file + " ", "")
            second_file = command_body
            if self.__dir_in_root(second_file):
                if self.__dir_in_root(first_file):
                    shutil.move(first_file, second_file)
                elif self.__not_path(first_file):
                    shutil.move(self.temp_dir + "/" + first_file, second_file)
            else:
                print("Место назначения должно быть директорией с прописанным путем.")
        except Exception as e:
            print("Файла не существует.")

    def rename(self, command):
        """
        Метод переименовывания указаного файла на указанное название"
        :param command: String
        """
        try:
            command_body = command.replace("rename ", "")
            first_file = command_body[:command_body.find(" ")]
            command_body = command_body.replace(first_file + " ", "")
            filesecond_file = command_body
            if self.__not_path(first_file) and self.__not_path(filesecond_file):
                os.rename(self.temp_dir + "/" + first_file, self.temp_dir + "/" + filesecond_file)
                print("Файл переименован")
            else:
                print("Файла не существует.")
        except Exception as e:
            print("Файла не существует.")

    def ls(self):
        """
        Метод выводя содержимого директории
        """
        for entity_name in os.listdir(path=self.temp_dir):
            print(entity_name)

    def help(self):
        """
        Метод вывода списка команд
        """
        print(self.help_text)


