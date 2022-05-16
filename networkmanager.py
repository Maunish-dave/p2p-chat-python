import socket


class NetworkManager():

    def __init__(self) -> None:
        self.username_port = {}
        self.port = 9999
        self.hostname = ''
        self.maxconnection = 99

    def start_manager(self):
        sc = socket.socket()
        sc.bind((self.hostname, self.port))
        sc.listen(self.maxconnection)

        while True:
            clientsocket, _ = sc.accept()
            message = clientsocket.recv(1024).decode()
            _, username, port = message.split(":")

            if "username" in message:
                self.username_port[username] = port
            elif "list" in message:
                userlist = ','.join([str(x) + ":" + str(y)
                                    for x, y in self.username_port.items()])
                clientsocket.send(userlist.encode())
            clientsocket.close()


if __name__ == "__main__":
    nm = NetworkManager()
    nm.start_manager()
