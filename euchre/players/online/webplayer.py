from euchre.players.player import Player
import abc
import socket
import json
import time

class WebPlayer(Player, abc.ABC):
    """A Player class that handles the TCP connection to a web player"""

    def __init__(self, host='localhost', port=6001, name='WebPlayer'):
        Player.__init__(self, name)
        self.host = host
        self.port = port
        self.last_hearbeat = curr_time
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

    # def sendMessage(self, message):
    #     """Send a TCP message to the player."""
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #         # connect to the worker
    #         sock.connect((self.host, self.port))
    #         # send a message
    #         message = json.dumps(message)
    #         sock.sendall(message.encode('utf-8'))
