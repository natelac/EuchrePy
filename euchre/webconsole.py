import socket
import json
import threading
import time
import click

from euchre.utils import messageToDictionary
from euchre.utils import printCards
from euchre.cards import Card

class WebConsole:
    def __init__(self, host, port, server_host, server_port, server_hb_port):
        self.socket_info = {
            'host': host,
            'port': int(port),
            'server_host': server_host,
            'server_port': int(server_port),
            'server_hb_port': int(server_hb_port)
        }

        # Game info
        #TODO: these need to be reset after each round
        #       played_cards just fills endlessly right now
        self.game_info = {
            'hand': None,
            'top_card': None,
            'trump': None,
            'played_cards': []
        }

        # Threading
        self.signals = {"shutdown": False}
        listen_thread = threading.Thread(
                target=self.listen,
                args=(self.signals,))
        listen_thread.start()

        self.sendMessage({"message_type": "register"})

        self.signals["shutdown"] = False

        # Halts this flow until listen_thread gets shutdown message
        listen_thread.join()

    def sendMessage(self, message):
        """Send TCP message to server"""
        message['player_host'] = self.socket_info['host']
        message['player_port'] = self.socket_info['port']
        #print("Message being sent:", message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.socket_info['server_host'],
                          self.socket_info['server_port']))
            message = json.dumps(message)
            sock.sendall(message.encode('utf-8'))

    def listen(self, signals):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.setSocket(sock)
            self.listenLoop(sock, signals)

    def listenLoop(self, sock, signals):
        """Listen and handle messages over a TCP connection"""
        while not self.signals["shutdown"]:
            message_dict = messageToDictionary(sock)

            def orderUp():
                printCards(self.game_info['hand'])
                ans = input('Order up? y/n\n')
                self.sendMessage({
                    'message_type': 'response',
                    'response_type': 'order_up',
                    'response': ans
                    })

            def orderTrump():
                ans = input('Call trump? y/n\n')
                self.sendMessage({
                    'message_type': 'response',
                    'response_type': 'order_trump',
                    'response': ans
                    })

            def callTrump():
                ans = input('Enter suit to pick\n')
                while ans not in ['C', 'S', 'H', 'D'] \
                        and ans != self.game_info['top_card'].suit:
                    ans = input('Not a valid suit.\n')
                self.sendMessage({
                    'message_type': 'response',
                    'response_type': 'call_trump',
                    'response': ans
                    })

            def goAlone():
                ans = input('Go alone? y/n\n')
                self.sendMessage({
                    'message_type': 'response',
                    'response_type': 'go_alone',
                    'response': ans
                    })

            def playCard():
                # Print trump and cards
                print("Trump Suit:", self.game_info['trump'])
                printCards(self.game_info['hand'])

                # Get card to play from user
                cards = [str(card) for card in self.game_info['hand']]
                ans = input('Enter card to play\n')
                while ans not in cards:
                    ans = input('Not a card in your hand.\n')

                # Remove card from hand, add to playedCards
                cardIndex = cards.index(ans)
                card = self.game_info['hand'].pop(cardIndex)
                self.game_info['played_cards'].append(card)

                #self._playedCards.append(card)
                self.sendMessage({
                    'message_type': 'response',
                    'response_type': 'play_card',
                    'response': ans
                })

            def updateHandMsg():
                self.game_info['hand'] = message_dict['new_hand']
                self.game_info['hand'] = \
                    [Card.str2card(card) for card in self.game_info['hand']]
                #printCards(self.game_info['hand'])

            def pointsMsg():
                team1 = message_dict['team1']
                team2 = message_dict['team2']
                print(f"{team1['players'][0]}, {team1['players'][1]} have "
                    f"{team1['points']}\t{team2['players'][0]},"
                    f"{team2['players'][1]} have {team2['points']}")

            def dealerMsg():
                dealer = message_dict['dealer']
                print(f"The dealer is {dealer}")

            def topCardMsg():
                top_card = message_dict['top_card']
                self.game_info['top_card'] = Card.str2card(top_card)
                print(f"The top card is {top_card}")

            def deniedUpMsg():
                denier = message_dict['denier']
                print(f"{denier} denied ordering up")

            def orderedUpMsg():
                orderer = message_dict['orderer']
                top_card = message_dict['top_card']
                print(f"{orderer} ordered up {top_card}")

            def deniedTrumpMsg():
                denier = message_dict['denier']
                print(f"{denier} denied ordering trump")

            def orderedTrumpMsg():
                orderer = message_dict['orderer']
                trump_suit = message_dict['trump_suit']
                print(f"{orderer} chose {trump_suit} as the trump suit")

            def misdealMsg():
                print("Misdeal, new dealer")

            def leaderMsg():
                leader = message_dict['leader']
                print(f"{leader} starts the first trick")

            def playedMsg():
                player = message_dict['player']
                card = Card.str2card(message_dict['card'])
                print(f"{player} played {card.prettyString()}")

            def takerMsg():
                taker = message_dict['taker']
                print(f"{taker} takes the hand")

            def penaltyMsg():
                player = message_dict['player']
                card = message_dict['card']
                print(
                f"{player} reneged by playing {card} and your team was awarded 2 points")

            def invalidSuitMsg():
                print("Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")

            def trickStartMsg():
                print()

            def newTrumpMsg():
                self.game_info['trump'] = message_dict['trump']
                #print(f"The trump is {self.game_info['trump']}")

            def takerMsg():
                print(f"{message_dict['taker']} takes the trick")

            def roundResults():
                winners = message_dict['winners']
                points_scored = message_dict['points_scored']
                team_tricks = message_dict['tricks_taken']
                print("{} and {} win the round with {} points and {} trick taken"
                      .format(winners[0], winners[1],
                              points_scored, team_tricks))

            if message_dict == -1:
                continue

            info_options = {
                'update_hand': updateHandMsg,
                'points': pointsMsg,
                'dealer': dealerMsg,
                'top_card': topCardMsg,
                'denied_up': deniedUpMsg,
                'ordered_up': orderedUpMsg,
                'ordered_trump': orderedTrumpMsg,
                'denied_trump': deniedTrumpMsg,
                'misdeal': misdealMsg,
                'leader': leaderMsg,
                'card_played': playedMsg,
                'renege': penaltyMsg,
                'invalid_suit': invalidSuitMsg,
                'trick_start': trickStartMsg,
                'new_trump':  newTrumpMsg,
                'taker': takerMsg,
                'round_results': roundResults,
            }

            request_options = {
                'order_up': orderUp,
                'order_trump': orderTrump,
                'call_trump': callTrump,
                'go_alone': goAlone,
                'play_card': playCard,
            }
            #print("Message from server:", message_dict)

            if message_dict['message_type'] == 'info':
                info_options[message_dict['info_type']]()
            elif message_dict['message_type'] == 'request':
                request_options[message_dict['request_type']]()

    def setSocket(self, sock):
        """Bind the socket to the server."""
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.socket_info["host"], self.socket_info["port"]))
        sock.listen()
        sock.settimeout(1)

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
