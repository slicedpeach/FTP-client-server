from socket import *
import random
import sys
import os

servername = "127.0.0.1"
serverport = 2121
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind((servername,serverport))
serversocket.listen()
print("server listening ...")
conectionsock, addr = serversocket.accept()
print("connection established!")


def ls():
    cwd = os.getcwd()
    f = []
    for (dirpath, dirnames, filenames) in os.walk(cwd):
        f.extend(filenames)
        break
    res = ""
    for i in dirnames:
        res = res+">"+i+"\n"
    for i in filenames:
        res = res+i+"\n"
    res += "-------------\ntotal size:"+str(get_dir_size())+" B"
    conectionsock.send(res.encode())


def pwd():
    cwd = os.getcwd()
    conectionsock.send(cwd.encode())


def cd(_path):
    dirs = [name for name in os.listdir('.') if os.path.isdir(os.path.join('.', name))]
    if _path not in dirs and not "..":
        print("directory does not exist!")
        conectionsock.send("Directory Not Found.".encode())
    else:
        os.chdir(_path)
        cwd = os.getcwd()
        res = f"successfully changed directory to:{cwd}!"
        conectionsock.send(res.encode())


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def download_file(_path):
    filenames = os.listdir()
    if _path in filenames:
        downsocket = socket(AF_INET, SOCK_STREAM)
        dport = random.randrange(3000, 50000)

        conectionsock.send(str(dport).encode())
        downsocket.bind((servername, dport))
        downsocket.listen()

#        f = open(_path, 'rb')

        print("waiting for download...")

        downloadsock, daddress = downsocket.accept()
        print("download pending...")
        with open(_path ,'rb') as file:
            print(f"downloading file: {_path}")
            downloadsock.sendall(file.read())
#            res = conectionsock.recv(1024).decode()
#            print(res)
#        if res=="done":
            file.close()
            downloadsock.close()
            print("download complete!")

    else:
        res = "Bad Request file not found!"
        conectionsock.send(res.encode())
        print(res)


while True:
    print("waiting for command...")
    message = conectionsock.recv(1024).decode()
    print("command recieved:")
    if message == "list" or message == "LIST":
        print("List files in directory")
        ls()
    elif message =="pwd" or message =="PWD":
        print("view current directory")
        pwd()
    elif message == "quit":
        print("Thanks for giving it a try")
        conectionsock.close()
        break
    elif message == "help" or message == "HELP":
        print("show help")
        conectionsock.send("help".encode())
    elif message.startswith("cd") or message.startswith("CD"):
        print("change directory")
        cd(message[3:])
    elif message.startswith("dwld") or message.startswith("DWLD"):
        print("download file")
        download_file(message[5:])
    else:
        conectionsock.send("invalid input".encode())


#    conectionsock.send(message.encode())
