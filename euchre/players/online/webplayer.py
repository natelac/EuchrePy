import abc
import socket
import json
import time

from euchre.players.player import Player
from euchre.cards.card import Card


class WebPlayer(Player, abc.ABC):
    """A Player class for TCP connected players.

    Allows the server to communicate with players over the web.

    DOES NOT validate player responses.

    Attributes:
        updates (dict):
            'new_update' (bool): Whether there is an un-processed response
            'response_type' (str): Type of the response
                    NOTE: This is NOT the value type
            'response' (?): Value dependent on the response type
        host (str): The name of the host
        port (int): The port of the host
        last_heartbeat (time): Time that the last heartbeat was recieved
            from the client
    """

    def __init__(self, host='localhost', port=6001, name='WebPlayer'):
        Player.__init__(self, name)
        self.updates = {
            'new_update': False,
            'response_type': None,
            'response': None
        }
        self.host = host
        self.port = int(port)
        self.last_heartbeat = time.perf_counter()

    @property
    def address(self):
        """The host:port address of the player

        Returns:
            (str): String address of the player
        """
        return str(self.host) + ":" + str(self.port)

    @classmethod
    def getAddress(cls, host, port):
        """Convert host:port pair to string.

        Args:
            host (str): Host
            port (int): Host port
        """
        return str(host) + ":" + str(port)

    # Networking methods
    # -------------------------------------------------------------------------

    def recvMessage(self, message):
        """Recieves a TCP message from a client.

        Currently only takes message that are a response to a gameplay
        related request, therefore it ignores the 'message_type'.

        Args:
            message (dict):
                # Response messages
                'message_type' (str): Type of the message, 'response'
                'response_type' (str): Type of response, fx 'order_up'
                'response' (?): Response value
                # Other Messages

        """
        self.updates['new_update'] = True
        self.updates['response_type'] = message['response_type']
        self.updates['response'] = message['response']

    def sendMessage(self, message):
        """Send a TCP message to the player.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            message = json.dumps(message)
            sock.sendall(message.encode('utf-8'))

    def request(self, request_type):
        """Send a TCP request to the client and await a relevant response.
        """
        while True:
            # Send request to client
            self.sendMessage({'message_type': 'request',
                              'request_type': request_type})

            # Wait for response
            # Blocking is OK since game can't continue without client response
            while self.updates['new_update'] != True:
                time.sleep(0.1)

            if self.updates['response_type'] != request_type:
                # Invalid response
                print("Error: Incorrect update type recieved.")
                print(
                    f"Expected: {request_type}\nrecieved: {self.updates['response_type']}")
            else:
                # Valid response
                break

        # Return valid response
        self.updates['new_update'] = False
        return self.updates['response']

    # Decision methods that require a response from the client
    # -------------------------------------------------------------------------

    def orderUp(self):
        ans = self.request('order_up')
        return ans == 'y'

    def orderTrump(self):
        ans = self.request('order_trump')
        return ans == 'y'

    def callTrump(self, top_suit):
        ans = self.request('call_trump')
        while ans not in ['C', 'S', 'H', 'D'] and ans != top_suit:
            ans = self.request('call_trump')
        return ans

    def goAlone(self):
        ans = self.request('go_alone')
        return ans == 'y'

    def playCard(self, leader, cards_played, trump):
        ans = self.request('play_card')
        return Card.str2card(ans)

    def discardCard(self, top_card):
        ans = self.request('discard_card')
        return ans

    # Information updates that don't require a return value
    # -------------------------------------------------------------------------
    def updateHand(self, cards):
        self.hand = cards
        msg = {'message_type': 'info',
               'info_type': 'update_hand',
               'new_hand': [str(card) for card in cards]}
        self.sendMessage(msg)

    def pointsMsg(self, team1, team2):
        msg = {
            'message_type': 'info',
            'info_type': 'points',
            'team1': {
                'players': (str(team1._p1), str(team1._p2)),
                'points': team1.points
            },
            'team2': {
                'players': (str(team2._p1), str(team2._p2)),
                'points': team2.points
            }
        }
        self.sendMessage(msg)

    def dealerMsg(self, dealer):
        msg = {
            'message_type': 'info',
            'info_type': 'dealer',
            'dealer': str(dealer)
        }
        self.sendMessage(msg)

    def topCardMsg(self, top_card):
        msg = {
            'message_type': 'info',
            'info_type': 'top_card',
            'top_card': str(top_card)
        }
        self.sendMessage(msg)

    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        winners = taking_team.players
        msg = {
            'message_type': 'info',
            'info_type': 'round_results',
            'winners': (str(winners[0]), str(winners[1])),
            'points_scored': points_scored,
            'tricks_taken': team_tricks
        }
        self.sendMessage(msg)

    def orderedUpMsg(self, player, top_card):
        msg = {
            'message_type': 'info',
            'info_type': 'ordered_up',
            'orderer': str(player),
            'top_card': str(top_card)
        }
        self.sendMessage(msg)

    def deniedUpMsg(self, player):
        msg = {
            'message_type': 'info',
            'info_type': 'denied_up',
            'denier': str(player)
        }
        self.sendMessage(msg)

    def orderedTrumpMsg(self, player, trump_suit):
        msg = {
            'message_type': 'info',
            'info_type': 'ordered_trump',
            'orderer': str(player),
            'trump_suit': trump_suit
        }
        self.sendMessage(msg)

    def deniedTrumpMsg(self, player):
        msg = {
            'message_type': 'info',
            'info_type': 'denied_trump',
            'denier': str(player)
        }
        self.sendMessage(msg)

    def gameResultsMsg(self, winning_team):
        winners = winning_team.players
        msg = {
            'message_type': 'info',
            'info_type': 'game_results',
            'winners': (str(winners[0]), str(winners[1]))
        }
        self.sendMessage(msg)

    def misdealMsg(self):
        msg = {
            'message_type': 'info',
            'info_type': 'misdeal'
        }
        self.sendMessage(msg)

    def leaderMsg(self, leader):
        msg = {
            'message_type': 'info',
            'info_type': 'leader',
            'leader': str(leader)
        }
        self.sendMessage(msg)

    def playedMsg(self, player, card):
        msg = {
            'message_type': 'info',
            'info_type': 'card_played',
            'player': str(player),
            'card': str(card)
        }
        self.sendMessage(msg)

    def takerMsg(self, taker):
        msg = {
            'message_type': 'info',
            'info_type': 'taker',
            'taker': str(taker)
        }
        self.sendMessage(msg)

    def penaltyMsg(self, player, card):
        msg = {
            'message_type': 'info',
            'info_type': 'renege',
            'player': str(player),
            'card': str(card)
        }
        self.sendMessage(msg)

    def invalidSuitMsg(self):
        msg = {
            'message_type': 'info',
            'info_type': 'invalid_suit'
        }
        self.sendMessage(msg)

    def trickStartMsg(self):
        msg = {
            'message_type': 'info',
            'info_type': 'trick_start'
        }
        self.sendMessage(msg)

    def newTrumpMsg(self, trump):
        msg = {
            'message_type': 'info',
            'info_type': 'new_trump',
            'trump': trump
        }
        self.sendMessage(msg)

    def orderUpMsg(self, player, top_card):
        msg = {
            'message_type': 'info',
            'info_type': 'ordered_up',
            'orderer': str(player),
            'top_card': str(top_card)
        }
        self.sendMessage(msg)
