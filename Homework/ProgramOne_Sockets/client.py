import sys
import socket
import threading

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
    sys.stdout.write('[Me] '); sys.stdout.flush()
    thread = threading.Thread(target=recieveData(), args=())
    thread_two = threading.Thread(target=send_messages(), args=())
    thread.start()
    thread_two.start()


def send_messages():

    msg = sys.stdin.readline()
    client_socket.send(msg)


def recieveData():

    # Poll for data
    while True:
        data, addr = client_socket.recv(4196)  # 4196

        print(data)

    client_socket.close()


if __name__ == "__main__":

    sys.exit(client())
