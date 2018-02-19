import sys
import socket
from threading import Thread
import select
import time


class Client:

    def __init__(self, host, port):
        self._HOST = host
        self._PORT = port
        self._read_socket = []
        self._PROTOCOL_PHASE = None
        self._WS = " "
        self._M_TYPE = None
        self._PROBES = 15
        self._LOOP = 1
        self._MSG_SIZE = 0
        self._SERVER_DELAY = 5
        self._PAYLOAD = ""
        self._RTT_array = []
        self._t1_check = 0
        self._t0_check = 0

    def connect(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._client_socket.connect((self._HOST, self._PORT))
            print('Connected to: ' + self._HOST)
            self._client_socket.setblocking(0)
            self._read_socket.append(self._client_socket)

        except socket.error as errmsg:
            print('Caught exception socket.error: %s' % errmsg)
            sys.exit()

    def close_connection(self):
        print("Closing Connection...")
        self._PROTOCOL_PHASE = 't'
        msg_str = self._PROTOCOL_PHASE
        self._client_socket.send(msg_str.encode())
        self._recieveThread.join()
        self._client_socket.close()
        sys.exit(0)
        sys.exit(0)

    def run(self):
        self._recieveThread = Thread(target=self.recieveData)
        self._recieveThread.start()
        while self._LOOP < 13:
            print('Sending initial probe for trial: ' + str(self._LOOP))
            print("Message size: " + str(self._MSG_SIZE))
            startup_msg = self.build_startup_message()
            self._client_socket.send(startup_msg.encode())
            print('Starting Threads...')
            self.probe_server()
            self._LOOP = self._LOOP + 1
            self.log_data()
        self.close_connection()

    def probe_server(self):
        self.build_measurement_message()
        for protocol_sequence_number in range(self._PROBES):
            # print("Sent probe number: " + str(protocol_sequence_number + 1))
            msg = " "
            # things keep happening out of order without the artificial delay
            time.sleep(0.1 + self._SERVER_DELAY)
            msg = self._PROTOCOL_PHASE + self._WS + str(protocol_sequence_number) \
                + self._WS + self._PAYLOAD + self._WS + str(time.time())
            print("Sending data")
            self._client_socket.send(msg.encode())

    def recieveData(self):
        print("Beginning recieve thread...\n")
        # Poll for data
        while True:
            ready_to_read, ready_to_write, in_error = select.select(
                self._read_socket, [], [], 0)
            try:
                for s in ready_to_read:
                    # recv'd data must be decoded before being presented as text
                    # had to make a ridiculous buffer so that I didnt have to make a new
                    # socket every time...
                    data = self._client_socket.recv(999999999).decode()
                    if data:
                        # print("\n")
                        # print(data)
                        print("Recieved Data.")
                        rtt = self.handle_time(data)
                        self._RTT_array.append(rtt)
                        data = " "

            except socket.error as errmsg:
                print("Socket error caught: %s" % errmsg)

            # except ValueError:
                # print("The connection was closed. No longer listening.")
            continue

    def handle_time(self, msg):
        msg_array = msg.split()
        t0 = msg_array[3]
        t1 = msg_array[4]
        rtt = float(t1) - float(t0)
        return rtt

    def log_data(self):
        print("Logging")
        log_file = open("rtt.txt", "a")
        log_file.write(socket.gethostname() + "\n")
        log_file.write("Message type: " + self._M_TYPE + "\n")
        log_file.write("Number of Probes: " + str(self._PROBES) + "\n")
        log_file.write("Message size: " + str(self._MSG_SIZE) + " bytes" + "\n")
        log_file.write("Server delay: " + str(self._SERVER_DELAY) + "\n")
        # get average RTT time
        log_file.write("RTTs: " + str(self._RTT_array))
        rtt_average = sum(self._RTT_array) / int(len(self._RTT_array))
        log_file.write("RTT Average: " + str(rtt_average) + "\n")
        print("RTT Average: " + str(rtt_average) + "\n")
        throughput = self._MSG_SIZE / rtt_average
        log_file.write("Throughput: " + str(throughput) + " bytes/second" + "\n")
        log_file.close()
        self._RTT_array = []

    def build_startup_message(self):
        print("Building Protocol Phase Message: s")
        self._PROTOCOL_PHASE = 's'
        # self.getMType()
        # self.getProbeNum()
        self.getMsgSize()
        # self.getServerDelay()
        msg_str = " "
        msg_str = self._PROTOCOL_PHASE + self._WS + self._M_TYPE + self._WS + \
            str(self._PROBES) + self._WS + str(self._MSG_SIZE) + self._WS + str(self._SERVER_DELAY) + "\n"
        return msg_str

    def build_measurement_message(self):
        print("Building Protocol Phase Message: m")
        self._PROTOCOL_PHASE = 'm'
        # build message of giving size
        for i in range(self._MSG_SIZE):
            self._PAYLOAD = self._PAYLOAD + "1"

    def getMType(self):
        inputText = input("Enter Message Type (rtt or tput): ")
        if inputText == "rtt" or "tput":
            self._M_TYPE = inputText
        else:
            print("Invalid Message Type")
            self.getMType()

    def getProbeNum(self):
        inputNumber = input("Enter Number of Probes (integer): ")
        try:
            inputNumber = int(inputNumber)
            self._PROBES = inputNumber
        except ValueError:
            print("Enter a valid integer.")
            self.getProbeNum()

    def getMsgSize(self):
        if self._LOOP == 1:
            self._MSG_SIZE = 1
            self._M_TYPE = "rtt"
        elif self._LOOP == 2:
            self._MSG_SIZE = 100
            self._M_TYPE = "rtt"
        elif self._LOOP == 3:
            self._MSG_SIZE = 200
            self._M_TYPE = "rtt"
        elif self._LOOP == 4:
            self._MSG_SIZE = 400
            self._M_TYPE = "rtt"
        elif self._LOOP == 5:
            self._MSG_SIZE = 800
            self._M_TYPE = "rtt"
        elif self._LOOP == 6:
            self._MSG_SIZE = 1000
            self._M_TYPE = "rtt"
        elif self._LOOP == 7:
            self._MSG_SIZE = 2**10
            self._M_TYPE = "tput"
        elif self._LOOP == 8:
            self._MSG_SIZE = 2 * (2**10)
            self._M_TYPE = "tput"
        elif self._LOOP == 9:
            self._M_TYPE = "tput"
            self._MSG_SIZE = 4 * (2**10)
            self._M_TYPE = "tput"
        elif self._LOOP == 10:
            self._MSG_SIZE = 8 * (2**10)
            self._M_TYPE = "tput"
        elif self._LOOP == 11:
            self._MSG_SIZE = 16 * (2**10)
            self._M_TYPE = "tput"
        elif self._LOOP == 12:
            self._MSG_SIZE = 32 * (2**10)
            self._M_TYPE = "tput"

    def getServerDelay(self):
        inputNumber = input("Enter Server Delay (seconds, float): ")
        try:
            inputNumber = float(inputNumber)
            self._SERVER_DELAY = inputNumber
        except ValueError:
            print("Enter a valid float.")
            self.getServerDelay()
