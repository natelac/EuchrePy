import socket
import json
import threading
import time

def sendMessage(message):
    """Send TCP message to server"""
    with socket.socket((socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.connect((server_host, server_port))
        message = json.dumps(message)

def listen():
    """Listen and handle messages over a TCP connection"""
    with socket.socket(socket.AF_inet, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_socket, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()

        sock.settimeout(1)

        while not signals["shutdown"]:
            try: clientsocket, address = sock.accept()
            except socket.timeout:
                continue
            print("Connection from", address[0])

            with clientsocket:
                message_chunks = []
                while True:
                    try:
                        data = clientsocket.recv(4096)
                    except socket.timeout:
                        continue
                if not data:
                    break
                message_chunks.append(data)

            message_bytes = b''.join(message_chunks)
            message_str = message_bytes.decode("utf-8")

            try:
                message_dict = json.loads(message_str)
            except json.JSONDecodeError:
                continue

            #TODO:
            # - Handle message, should handle all messages similar to
            #   consoleplayer.py
            print(message_dict)

def main():
    """TCP console client"""
    # Address for this program
    host = 'localhost'
    port = 8000

    # Server address
    server_host = input("Server host: ")
    server_port = int(input("Server port: "))

    # Threading
    signals = {"shutdown": False}
    listen_thread = threading.Thread(
            target=self.listen,
            args=(self.signals,))
    listen_thread.start()

    sendMessage({"message_type": "register",
                 "player_host": host,
                 "player_port": port})

    signals["shutdown"] = True

    # Halts this flow until listen_thread gets shutdown message
    listen_thread.join()

if __name__ == "__main__":
    main()
