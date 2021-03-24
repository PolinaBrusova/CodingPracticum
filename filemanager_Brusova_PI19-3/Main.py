import configparser
import Manager

config = configparser.ConfigParser()
config.read('config.ini')

manager = Manager.FileManager(config["settings"]["WORKING_DIRECTORY"], config["settings"]["HELP_TEXT"])

while True:
    try:
        value = input("$"+manager.getCurrent()[manager.getCurrent().rfind("/")+1:]+">")
        if value.startswith("create "):
            manager.create(value)
        elif value.startswith("delete "):
            manager.delete(value)
        elif value.startswith("goto"):
            manager.cd(value)
        elif value.startswith("make "):
            manager.touch(value)
        elif value.startswith("write "):
            manager.write(value)
        elif value.startswith("read "):
            manager.read(value)
        elif value.startswith("copy "):
            manager.copy(value)
        elif value.startswith("move "):
            manager.move(value)
        elif value.startswith("rename "):
            manager.rename(value)
        elif value == "files":
            manager.ls()
        elif value == "help":
            manager.help()
        else:
            manager.manage_others()
    except KeyboardInterrupt as e:
        break
