from .Client import Client


def main(host, port):

    client = Client(host, port)
    client.connect()
    client.run()
    sys.exit()
