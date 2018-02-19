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
        self._PROTOCOL_PHASE
        self._WS = " "
        self._M_TYPE
        self._PROBES
        self._MSG_SIZE
        self._SERVER_DELAY = 0
        self._PAYLOAD = ""
        self._RTT_array = []

    def connect(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._client_socket.connect(self._HOST, self._PORT)
            print('Connected to: ' + self._HOST)
            self._client_socket.setblocking(0)
            self._read_socket.append(self._client_socket)

        except socket.error as errmsg:
            print('Caught exception socket.error: %s' % errmsg)
            sys.exit()

    def close_connection(self):
        self._PROTOCOL_PHASE = 't'
        msg_str = self._PROTOCOL_PHASE
        self._client_socket.send(msg_str.encode())
        self._log_data()
        self._client_socket.close()

    def log_data(self):
        log_file = open("rtt.log", "w")
        log_file.write(socket.gethostname() + "\n")
        log_file.write("Message type: " + self._M_TYPE + "\n")
        log_file.write("Number of Probes: " + self._PROBES + "\n")
        log_file.write("Message size: " + self._MSG_SIZE + " bytes" + "\n")
        log_file.write("Server delay: " + self._SERVER_DELAY + "\n")
        log_file.write("Data: " + self._RTT_array + "\n")
        # get average RTT time
        rtt_nums = [rtt[1] for rtt in self._RTT_array]
        rtt_average = sum(rtt_nums) / float(len(rtt_nums))
        log_file.write("Average: " + rtt_average + "\n")
        log_file.write("Througput: " + self._MSG_SIZE / rtt_average + " bytes/second" + "\n")
        log_file.close()

    def run(self):
        print('Sending initial probe...')
        startup_msg = self._build_startup_message()
        self._client_socket.send(startup_msg.encode())
        print('Starting Threads...')
        Thread(target=self.recieveData).start()
        Thread(target=self.send_packets).start()
        while True:
            self.probe_server()

    def build_startup_message(self):
        print("Building Protocol Phase Message: s\n")
        self._PROTOCOL_PHASE = 's'
        self._getMType()
        self._getProbeNum()
        self._getMsgSize()
        self._getServerDelay()
        msg_str = self._PROTOCOL_PHASE + self._WS + self._M_TYPE + self._WS + \
            str(self._PROBES) + self._WS + str(self._MSG_SIZE) + self._WS + str(self._SERVER_DELAY) + "\n"
        return msg_str

    def getMType(self):
        print("Enter Message Type (rtt or tput)")
        inputText = sys.std.readline()
        if inputText == "rtt" or inputText == "tput":
            self._M_TYPE == inputText
        else:
            print("Invalid Message Type")
            self._getMType()

    def getProbeNum(self):
        print("Enter Number of Probes (integer)")
        inputNumber = sys.std.readline()
        try:
            inputNumber = int(inputNumber)
            self._PROBES = inputNumber
        except ValueError:
            print("Enter a valid integer.")
            self._getProbeNum()

    def getMsgSize(self):
        print("Enter Size of Message (bytes)")
        inputNumber = sys.std.readline()
        try:
            inputNumber = int(inputNumber)
            self._MSG_SIZE = inputNumber
        except ValueError:
            print("Enter a valid integer.")
            self._getMsgSize()

    def getServerDelay(self):
        print("Enter Server Delay (seconds, float)")
        inputNumber = sys.std.readline()
        try:
            inputNumber = float(inputNumber)
            self._SERVER_DELAY = inputNumber
        except ValueError:
            print("Enter a valid float.")
            self._getServerDelay()

    def build_measurement_message(self):
        self._PROTOCOL_PHASE = 'm'
        # build message of giving size
        for i in range(self._MSG_SIZE):
            self._PAYLOAD = self._PAYLOAD + "1"

    def probe_server(self):
        for protocol_sequence_number in range(self._PROBES):
            print("Sent probe number: " + protocol_sequence_number)
            self._t0 = time.clock()
            self._t0_check = 1
            msg = self._PROTOCOL_PHASE + self._WS + protocol_sequence_number + self._WS + self._PAYLOAD + "\n"
            self._client_socket.send(msg.encode())

    def handle_time(self):
        if self._t1_check & self._t0_check == 1:
            self._t1 = 0
            self._t0 = 0
            self._RTT_array.append((self._t0, self._t1, self._t1 - self._t0))

    def recieveData(self):
        print("Beginning recieve thread...\n")
        # Poll for data
        while True:
            ready_to_read, ready_to_write, in_error = select.select(
                self._read_socket, [], [], 0)
            try:
                for s in ready_to_read:
                    # recv'd data must be decoded before being presented as text
                    data = self._client_socket.recv(4196).decode()
                    if data:
                        self._t1 = time.clock()
                        self._t1_check = 1
                        print("\n")
                        print(data)

            except socket.error as errmsg:
                print("Socket error caught: %s" % errmsg)
                continue

        self._client_socket.close()
