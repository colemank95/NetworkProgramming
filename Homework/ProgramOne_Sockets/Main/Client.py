import sys
import socket
from threading import Thread


class Client:

    def __init__(self, host, port):

        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._client_socket.connect((host, port))

        except socket.error as errmsg:
            print('Caught exception socket.error: %s' % errmsg)
            sys.exit()

        print('Connected')
        sys.stdout.write('[Me] ')
        sys.stdout.flush()

    def run(self):
        print('Starting Threads')
        Thread(target=self.send_messages()).start()
        Thread(target=self.recieveData()).start()
        print('You can now chat...')
        while True:
            self._send_messages()

    def send_messages(self):
        msg = sys.stdin.readline()
        self._client_socket.send(bytes(msg, 'UTF-8'))
        sys.stdout.write('[Me] ')
        sys.stdout.flush()

    def recieveData(self):
        print("Beginning recieve thread...\n")
        # Poll for data
        while True:
            data = self._client_socket.recv(4196).decode('UTF-8')
            if data:
                print(data)
            continue

        self._client_socket.close()
