import sys
import socket
import threading
from threading import Thread


class Client:

    def __init__(self, host, port):

        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._client_socket.connect((host, port))

        except socket.error, exc:
            print('Caught exception socket.error: %s' % exc)
            sys.exit()

        print('Connected')
        sys.stdout.write('[Me] ')
        sys.stdout.flush()

    def run(self):
        Thread(target=self.send_messages()).start()
        Thread(target=self.recieveData()).start()

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

        self._client_socket.close()
