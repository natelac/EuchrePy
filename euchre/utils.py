"""Utils file.

This file is to house code common between the Server and the Players

"""
import json
import socket


def message_to_dictionary(sock):
    """Turn message received by sock to dictionary."""
    try:
        clientsocket, _ = sock.accept()
    except socket.timeout:
        return -1

    # Handle message recieved
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
        return -1

    return message_dict