"""Utils file.

Houses code common between the Server and the Players
"""
import json
import socket


def message_to_dictionary(sock):
    """Turn message received by sock to dictionary.

    Args:
        sock (socket.socket): Socket to listen to

    Returns:
        message_dict (int / dict): -1 if no socket, else the message as
            a python dictionary
    """
    # Listen for message
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


def printCards(cards):
    """Prints a 'nice' view of player's hand to console.
    """
    print('Cards: ', end="")
    pretty_cards = []
    for card in cards:
        pretty_cards.append(card.prettyString())
    print(*pretty_cards, sep=", ")
