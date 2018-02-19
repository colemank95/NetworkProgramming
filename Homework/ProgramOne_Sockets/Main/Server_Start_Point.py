from .Server import Server


def main():
    server = Server()
    server.build()
    server.run()
    sys.exit()
