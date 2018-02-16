import socket
import sys
from threading import Thread
import select

# define some frequently used variables
PORT = 58686
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
        # the select object is necessary in python to prevent connection errors
        # caused by trying to recv data on a socket that has no data buffered
        # ready_to_read is a list of sockets in the socket_list
        # that has buffered data ready to be recv'd
        ready_to_read, ready_to_write, in_error = select.select(
            socket_list, [], [], 0)
        for s in ready_to_read:
            if s != server_socket:
                msg = s.recv(4096).decode()
                if msg:
                    send_messages(server_socket, s, msg)
                    print(msg)
        continue


def accept_connections():
    # handles new connections
    while True:
        print("Waiting for a connection...")
        new_socket, new_socket_addr = server_socket.accept()
        print("New connection with: " + str(new_socket_addr))
        new_socket.setblocking(0)
        socket_list.append(new_socket)


def send_messages(server_socket, sender_socket, msg):
    # broadcast messages to clients
    for s in socket_list:
        if s != server_socket and s != sender_socket:
            # python3.x requires text strings to be encoded
            # before being sent as byte streams
            s.send(msg.encode())


if __name__ == "__main__":
    server()
