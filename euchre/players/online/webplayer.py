from euchre.players.player import Player
from euchre.cards.card import Card
import abc
import socket
import json
import time

class WebPlayer(Player, abc.ABC):
    """A Player class for TCP connected players"""

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
        #TODO
        # - Add enum, or bool, or string or something for current player state,
        #   i.e., disconnected, timing out, timed out, etc.,
        #   At the very least, for i f they have timed out

    @property
    def address(self):
        """Access as player.address."""
        return str(self.host) + ":" + str(self.port)

    @classmethod
    def getAddress(cls, host, port):
        """Convert host:port pair to string."""
        # Worker.get_address(host, port)
        return str(host) + ":" + str(port)

    def recvMessage(self, message):
        """Recieves a message from a client"""
        self.updates['new_update'] = True
        self.updates['response_type'] = message['response_type']
        self.updates['response'] = message['response']

    def sendMessage(self, message):
        """Send a TCP message to the player."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            message = json.dumps(message)
            sock.sendall(message.encode('utf-8'))

    def request(self, request_type):
        """Send a request to the client, and awaits a relevant response"""
        #self.updates = {'new_update': False}
        self.sendMessage({'message_type': 'request',
                          'request_type': request_type})
        while self.updates['new_update'] != True:
            time.sleep(0.1)
        if self.updates['response_type'] != request_type:
            print("Error: Incorrect update type recieved.")
            print(f"Expected: {request_type}\nrecieved: {self.updates['response_type']}")
            self.updates['new_update'] = False
            self.request(request_type)
        self.updates['new_update'] = False
        return self.updates['response']

    def orderUp(self):
        ans = self.request('order_up')
        return ans == 'y'

    def orderTrump(self):
        ans = self.request('order_trump')
        return ans == 'y'

    def callTrump(self, topSuit):
        ans = self.request('call_trump')
        while ans not in ['C', 'S', 'H', 'D'] and ans != topSuit:
            #TODO: Update player they played an invalid suit
            ans = self.request('call_trump')
        return ans

    def goAlone(self):
        ans = self.request('go_alone')
        return ans == 'y'

    def playCard(self, leader, cardsPlayed, trump):
        # Get card to play from user
        ans = self.request('play_card')
        # while ans not in cards:
            # TODO: Update player that they played a card not in their hand
            # ans = self.request('play_card')

        # Remove card from hand, add to playedCards
        # cardIndex = cards.index(ans)
        # card = self.hand.pop(cardIndex)
        # self._playedCards.append(card)

        return Card.str2card(ans)

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
        winners = taking_team.getPlayers()
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

    def gameResultsMsg(self):
        msg = {
                'message_type': 'todo'
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
