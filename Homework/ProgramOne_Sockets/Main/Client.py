import sys
import socket
from threading import Thread


class Client:

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def connect(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._client_socket.connect((self._host, self._port))
            print('Connected to: ' + self._host)

        except socket.error as errmsg:
            print('Caught exception socket.error: %s' % errmsg)
            sys.exit()

    def run(self):
        print('Starting Threads')
        Thread(target=self.recieveData).start()
        Thread(target=self.send_messages).start()
        print('You can now chat...')
        while True:
            self.send_messages()

    def send_messages(self):
        sys.stdout.write('--> ')
        sys.stdout.flush()
        msg = sys.stdin.readline()
        self._client_socket.send(bytes(msg, 'UTF-8'))

    def recieveData(self):
        print("Beginning recieve thread...\n")
        # Poll for data
        while True:
            try:
                data = self._client_socket.recv(4196).decode('UTF-8')

            except socket.error as errmsg:
                print('Caught exception socket.error: %s' % errmsg)
                sys.exit(1)

            if data:
                print(data)
            continue

        self._client_socket.close()
