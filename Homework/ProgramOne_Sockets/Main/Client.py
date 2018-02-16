import sys
import socket
from threading import Thread
import select


class Client:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._read_socket = []

    def connect(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._client_socket.connect((self._host, self._port))
            print('Connected to: ' + self._host)
            self._client_socket.setblocking(0)
            self._read_socket.append(self._client_socket)

        except socket.error as errmsg:
            print('Caught exception socket.error: %s' % errmsg)
            sys.exit()

    def run(self):
        print('Starting Threads')
        Thread(target=self.recieveData).start()
        Thread(target=self.send_messages).start()
        print('You can now chat...')
        # formatting for the chat terminal
        sys.stdout.write('--> ')
        sys.stdout.flush()
        while True:
            self.send_messages()

    def send_messages(self):
        msg = sys.stdin.readline()
        msg = "From " + socket.gethostname() + ": " + msg
        # similar to the .encode() function
        # text must be encoded to bytes before being sent
        self._client_socket.send(bytes(msg, 'UTF-8'))
        sys.stdout.write('--> ')
        sys.stdout.flush()

    def recieveData(self):
        print("Beginning recieve thread...\n")
        # Poll for data
        while True:
            ready_to_read, ready_to_write, in_error = select.select(
                self._read_socket, [], [], 0)
            try:
                for s in ready_to_read:
                    # recv'd data must be decoded before being presented as text
                    data = self._client_socket.recv(4196).decode('UTF-8')
                    if data:
                        print("\n")
                        print(data)
                        sys.stdout.write('--> ')
                        sys.stdout.flush()
            except socket.error as errmsg:
                # can't print out this message because it spams constantly
                #
                print("Socket error caught: %s" % errmsg)
                continue

        self._client_socket.close()
