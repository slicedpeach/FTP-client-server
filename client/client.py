from socket import *

servername = "0.tcp.eu.ngrok.io"
serverport = 2121
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((servername, 11116))
def download_file(_name,_port):
    if not _port=="Bad Request file not found!":
        dport = int(_port)
        print("connecting")
        clientdownsocket = socket(AF_INET, SOCK_STREAM)
        clientdownsocket.connect((servername,dport))
        print(f"downloading file:{_name}")
        with open(_name,'wb') as f:
            data = b""
            while True:
                ndata = clientdownsocket.recv(1024)
                data += ndata
#                print(data.decode())
                if not ndata:
#                    clientSocket.send("done".encode())
                    break
            f.write(data)
#            clientSocket.send("done".encode())
            print("download complete!")
            f.close()
            clientdownsocket.close()
    else:
        print(_port)


def ftphelp():
    instr = ["HELP", "LIST", "PWD", "CD dir_name", "DWLD file_path", "QUIT"]
    res = [":Show this help",
           ":List files",
           ":Show current directory",
           ":Change directory",
           ":Download file",
           ":Exit",
           ]
    print("welcome to the FTP simulator client!\n")
    print("Built by Saman Salmanzadeh!")
    print("call one of the following functions:")
    j = 0
    for i in instr:
        print(f"{i:<20}{res[j]:<20}")
        j += 1


ftphelp()
while True:
    message = input("command:")
    clientSocket.send(message.encode())
    if not message.startswith("cd") or not message.startswith("CD") or not message.startswith("dwld") or not message.startswith("DWLD"):
        modifiedmessage = clientSocket.recv(1024).decode()

    if message == "LIST" or message == "list":
        print(modifiedmessage)

    elif message == "pwd" or message == "PWD":
        print(modifiedmessage)
    elif message == "help" or message == "HELP":
        ftphelp()
    elif message.startswith("cd") or message.startswith("CD"):
        print(modifiedmessage)
    elif message.startswith("dwld") or message.startswith("DWLD"):
        download_file(message[5:],modifiedmessage)

    elif message == "quit" or message == "QUIT":
        clientSocket.close()
        break
    else:
        print("invalid input please enter a valid command!")
        ftphelp()
        #clientSocket.send("error".encode())
