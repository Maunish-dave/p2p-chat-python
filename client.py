import socket
import random
import threading
import time 
from contextlib import closing


class Client:

    def __init__(self) -> None:
        self.manager_port = 9999
        self.manager_hostname = ''
        self.port = None
        self.username = None
        self.hostname = ''
        self.register = False
        self.maxconnection = 99

        self.send_hostname = ''
        self.send_port = None

        self.all_messages = []

        self.current_socket = None

        self.current_sockets = {}

    def generate_port_number(self):
        port = random.randint(1500, 2000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.hostname, port))

        # while socket is found open
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            while result == 0:
                port = random.randint(1500, 2000)
                result = sock.connect_ex((self.hostname, port))

        self.port = port

    
    def receive(self):

        def add_client(clientsocket):
            while True:
                sendmessage = clientsocket.recv(1024).decode()
                if sendmessage != "":
                    time.sleep(2)
                    print(sendmessage)
                    self.all_messages.append(sendmessage)

        sc = socket.socket()
        sc.bind(('',self.port))

        while True:
            sc.listen(self.maxconnection)
            (clientsocket,address) = sc.accept()
            t = threading.Thread(target = add_client,args=(clientsocket,))
            t.start()

    def connect(self,send_port):
        print("connected to port: ",send_port)
        self.send_port = send_port
        if self.current_sockets.get(self.send_port):
            self.current_socket = self.current_sockets[self.send_port]
        else:
            self.current_socket = socket.socket()
            self.current_socket.connect((self.send_hostname,self.send_port))
            self.current_sockets[self.send_port] = self.current_socket

        
    def send_message(self,message:str):
        self.current_socket.send((self.username + ":" + message).encode())
        self.all_messages.append("You:" + message)


    def set_username(self, username):
        self.username = username
        self.generate_port_number()
        s = socket.socket()
        s.connect((self.manager_hostname, self.manager_port))
        message = "username:" + self.username + ":" + str(self.port)
        s.send(message.encode())
        s.close()

    def get_user_list_from_manager(self):
        s = socket.socket()
        s.connect((self.manager_hostname, self.manager_port))
        message = "list:" + self.username + ":" + str(self.port)
        s.send(message.encode())
        received_message = s.recv(1024).decode()
        s.close()
        return received_message
