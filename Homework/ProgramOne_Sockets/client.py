import sys
import socket
import threading
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def client():

    if(len(sys.argv) != 3):
        print ('Incorrect arguments. usage: python client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port_num = int(sys.argv[2])
    try:
        client_socket.connect((host, port_num))

    except:
        print('Can not connect')
        sys.exit()

    print('Connected')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()


def send_messages():
    print("Sending message...\n")
    msg = sys.stdin.readline()
    client_socket.send(bytes(msg, 'UTF-8'))
    sys.stdout.write('[Me] ')
    sys.stdout.flush()


def recieveData():
    print("Beginning recieve thread...\n")
    # Poll for data
    while True:
        data = client_socket.recv(4196).decode('UTF-8')
        if data:
            print(data)

    client_socket.close()


if __name__ == "__main__":
    Thread(target=send_messages()).start()
    Thread(target=recieveData()).start()
    sys.exit(client())
