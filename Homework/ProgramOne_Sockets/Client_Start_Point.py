from .Client import Client


def main(host, port):

	client = Client(host, port)
	client.run()