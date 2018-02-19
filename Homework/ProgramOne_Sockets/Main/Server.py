import socket
from threading import Thread
import select
import sys


class Server:

    def __init__(self):
        self._PORT = 58686
        self._BUFFER_SIZE = 4096
        self._socket_list = []
        # duplicated list beacuse "select" doesn't like lists of tuples
        self._socket_read_list = []

    def build(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((socket.gethostname(), self._PORT))
        self._server_socket.listen(5)
        print('Socket Created')
        # this prevents us from losing our port every time we kill the process and restart it
        self._server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket_read_list.append(self._server_socket)
        self._socket_list.append(self._server_socket)

    def run(self):
        Thread(target=self._accept_connections).start()
        while True:
            # the select object is necessary in python to prevent connection errors
            # caused by trying to recv data on a socket that has no data buffered
            # ready_to_read is a list of sockets in the self._socket_list
            # that has buffered data ready to be recv'd
            ready_to_read, ready_to_write, in_error = select.select(
                self._socket_read_list, [], [], 0)
            for s in ready_to_read:
                if s != self._server_socket:
                    msg = s.recv(self._BUFFER_SIZE).decode()
                    if msg:
                        msg_array = msg.split()
                        socket_index = s.index()
                        if msg_array[0] == ['s']:
                            self._validate_initial_message(msg_array, socket_index)
                            self._handle_initial_message(
                                msg_array, socket_index)
                        if msg_array[0] == ['m']:
                            self._validate_measurement_message(msg_array, socket_index)
                            self._handle_measurement_message(msg_array, socket_index)
                            self._echo_messages(self._server_socket, s, msg)
                        if msg_array[0] == ['t']:
                            if len(msg_array) != 1:
                                self._send_failure(socket_index, 3)
                        print(msg)
            continue

    def validate_measurement_message(self, msg_array, socket_index):
        if msg_array[0] != 'm':
            self._send_failure(self._socket_list[socket_index], 2)
        if msg_array[1] != self._socket_list[socket_index][5] + 1:
            self._send_failure(self._socket_list[socket_index], 2)

    def handle_measurement_message(self, msg_array, socket_index):
        self._socket_list[socket_index][5] = self._socket_list[socket_index][5] + 1

    def handle_initial_message(self, msg_array, socket_index):
        # using tuples to store sockets along with their relevant information
        for element in msg_array:
            self._socket_list[socket_index].append(element)
        # setting up a way to track sequence numbers
        self._socket_list[socket_index][5] = 0
        self._send_success(self._socket_list[socket_index])

    def validate_initial_message(self, msg_array, socket_index):
        if msg_array[0] != 's':
            self._send_failure(self._socket_list[socket_index], 1)
        elif msg_array[1] != "rtt" | "tput":
            self._send_failure(self._socket_list[socket_index], 1)
        elif not isinstance(msg_array[2], int):
            self._send_failure(self._socket_list[socket_index], 1)
        elif not isinstance(msg_array[3], int):
            self._send_failure(self._socket_list[socket_index], 1)
        elif not isinstance(msg_array[4], float):
            self._send_failure(self._socket_list[socket_index], 1)
        else:
            # setting up a way to track sequence numbers
            self._socket_list[socket_index][5] = 0
            self._send_success(self._socket_list[socket_index])

    def send_failure(self, send_socket, failure_type):
        if failure_type == 1:
            msg = "404 ERROR: Invalid Connection Setup Message"
            send_socket.send(msg.encode())
            sys.exit()

        elif failure_type == 2:
            msg = "404 ERROR: Invalid Measurement Message"
            send_socket.send(msg.encode())
            sys.exit()

        elif failure_type == 3:
            msg = "404 ERROR: Invalid Connection Termination Message"
            send_socket.send(msg.encode())
            sys.exit()

    def send_success(self, send_socket):
        msg = "200 OK: Read"
        send_socket.send(msg.encode())

    def accept_connections(self):
        # handles new connections
        while True:
            print("Waiting for a connection...")
            new_socket, new_socket_addr = self._server_socket.accept()
            print("New connection with: " + str(new_socket_addr))
            new_socket.setblocking(0)
            self._socket_read_list.append(new_socket)
            self._socket_list.append(new_socket)

    def echo_messages(self, server_socket, sender_socket, msg):
        # broadcast messages to clients
        for s in self._socket_read_list:
            if s != self._server_socket and s != sender_socket:
                # python3.x requires text strings to be encoded
                # before being sent as byte streams
                s.send(msg.encode())
