import socket
import sys
from threading import Thread

# define some frequently used variables
PORT = 58681
BUFFER = 4096
# create a list to maintain all socket connections
socket_list = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), PORT))
server_socket.listen(5)
print('Socket Created')
# this prevents us from losing our port every time we kill the process and restart it
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_list.append(server_socket)

def server():
    Thread(target=accept_connections).start()
    while True:
        for s in socket_list:
            if s != server_socket:
                msg = s.recv(4096).decode()
                if msg:
                    send_messages(server_socket, s, msg)
                    print(msg)
        continue


def accept_connections():
    while True:
        print("Waiting for a connection...")
        new_socket, new_socket_addr = server_socket.accept()
        print("New connection with: " + str(new_socket_addr))
        socket_list.append(new_socket)


def send_messages(server_socket, sender_socket, msg):
    for s in socket_list:
        if s != server_socket and s != sender_socket:
            s.send(msg.encode())


if __name__ == "__main__":
    server()
