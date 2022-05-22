from euchre.players.player import Player
import abc
import socket
import json
import time

class WebPlayer(Player, abc.ABC):
    """A Player class for TCP connected players"""

    def __init__(self, updates, host='localhost', port=6001, name='WebPlayer'):
        Player.__init__(self, name)
        self.updates = updates # Dictionary for updating webplayer with new messages from client
        self.host = host
        self.port = port
        self.last_heartbeat = time.perf_counter()
        #TODO
        # - Add enum, or bool, or string or something for current player state,
        #   i.e., disconnected, timing out, timed out, etc.,
        #   At the very least, for if they have timed out

    @property
    def address(self):
        """Access as player.address."""
        return str(self.host) + ":" + str(self.port)

    @classmethod
    def getAddress(cls, host, port):
        """Convert host:port pair to string."""
        # Worker.get_address(host, port)
        return str(host) + ":" + str(port)

    def sendMessage(self, message):
        """Send a TCP message to the player."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            message = json.dumps(message)
            sock.sendall(message.encode('utf-8'))

    def request(self, request_type):
        """Send a request to the client, and awaits a relevant response"""
        self.updates = {'new_update': False}
        self.sendMessage({'message_type': 'request',
                          'request_type': request_type})

        while self.updates['new_update'] != True:
            sleep(0.05)
        if self.updates['request_type'] != request_type:
            print("Error: Incorrect update type recieved.")
            self.makeRequest(request_type)
        return self.updates['response']
