import socket
import json
import threading
import time
import click

from euchre.utils import message_to_dictionary

class WebConsole:
    def __init__(self, host, port, server_host, server_port, server_hb_port):
        self.host = host
        self.port = port
        self.server_host = server_host
        self.server_port = server_port
        self.server_hb_pjort = server_hb_port

        # Threading
        self.signals = {"shutdown": False}
        listen_thread = threading.Thread(
                target=self.listen,
                args=(self.signals,))
        listen_thread.start()

        self.sendMessage({"message_type": "register",
                     "player_host": self.host,
                     "player_port": self.port})

        self.signals["shutdown"] = False



        # Halts this flow until listen_thread gets shutdown message
        listen_thread.join()

    def sendMessage(self, message):
        """Send TCP message to server"""
        print("Message being sent:", message)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_host, self.server_port))
            message = json.dumps(message)
            sock.sendall(message.encode('utf-8'))

    def listen(self, signals):
        """Listen and handle messages over a TCP connection"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen()
            sock.settimeout(1)

            while not self.signals["shutdown"]:
                message_dict = message_to_dictionary(sock)

                if message_dict == -1:
                    continue

                #TODO:
                # - Handle message, should handle all messages similar to
                #   consoleplayer.py

                print("Message from server:", message_dict)


def playWebConsole():
    #TODO: So that euchrepy.runWebConsole() can be called
    pass



@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=6001)
@click.option("--server-host", "server_host", default="localhost")
@click.option("--server-port", "server_port", default=6000)
@click.option("--server-hb-port", "server_hb_port", default=5999)
def main(host, port, server_host, server_port, server_hb_port):
    """TCP console client"""
    WebConsole(host, port, server_host, server_port, server_hb_port)

if __name__ == "__main__":
    main()
