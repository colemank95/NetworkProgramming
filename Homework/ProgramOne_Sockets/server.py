import socket
import select
import sys

# define some frequently used variables
PORT = 58685
BUFFER = 4096
# create a list to maintain all socket connections
socket_list = []


def server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), PORT))
    server_socket.listen(5)

    # this prevents us from losing our port every time we kill the process and restart it
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    socket_list.append(server_socket)

    # socket.select() makes chat clients really easy in python
    read_objects, write_objects, errors = select.select(socket_list, [], [], 0)

    while True:
        # poll through each socket
        for s in socket_list:
            if s == server_socket:
                new_socket, new_socket_addr = server_socket.accept()
                socket_list.append(new_socket)
            else:
                text = s.recv(4096)

                if text:
                    print(text)
                    send_messages(server_socket, s, text)


def send_messages(server_socket, sender_socket, text):
    for s in socket_list:
        if s != server_socket and s != sender_socket:
            s.send(bytes(text, 'UTF-8'))


if __name__ == "__main__":

    sys.exit(server())
