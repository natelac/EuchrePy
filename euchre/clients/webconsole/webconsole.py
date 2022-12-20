import socket
import json
import threading
import time
import click

from euchre.utils import message_to_dictionary
from euchre.utils import printCards
from euchre.cards import Card

class WebConsole:
    """A console that can connect to a game of euchre over the web.

    TODO:
        - Separate 'switch' statements into separate functions / other files
        - Figure out consistency for signals vs self.signals
    """

    def __init__(self, host='localhost', port=0, server_host='localhost',
                 server_port=6000, server_hb_port=5999, name='WebConsole'):
        self.name = name
        self.socket_info = {
            'host': host,
            'port': int(port),
            'server_host': server_host,
            'server_port': int(server_port),
            'server_hb_port': int(server_hb_port)
        }

        # Game info
        self.game_info = {
            'hand': None,
            'top_card': None,
            'trump': None,
            'played_cards': []
        }

        # Threading
        self.signals = {"shutdown": False,
                        "request": None}
        self.threads = []

        # Create listening thread on socket 
        # TODO: Socket needs to be closed at some point
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket first before threading
        self.setSocket(sock)
        listen_thread = threading.Thread(
            target=self.listenLoop,
            args=(sock, self.signals,))
        listen_thread.start()
        self.threads.append(listen_thread)

        # Thread for player input
        decision_thread = threading.Thread(
            target=self.decisionLoop,
            args=(self.signals,))
        decision_thread.start()
        self.threads.append(decision_thread)

        print(self.socket_info['host'],
              self.socket_info['port'])
        self.registerWithServer() 

        # Halts this flow until listen_thread gets shutdown message
        listen_thread.join()
        decision_thread.join()

    def registerWithServer(self):
        self.sendMessage({
            "message_type": "register",
            "player_name": self.name
        })


    def handleRequest(self, request):
        """Process request from server and respond.

        Enables asynchronous player input and networking.
        """
        def orderUp():
            printCards(self.game_info['hand'])
            ans = input('Order up? y/n\n')
            if self.signals['shutdown']:
                print("Server closed")
                return
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'order_up',
                'response': ans
            })

        def orderTrump():
            ans = input('Call trump? y/n\n')
            if self.signals['shutdown']:
                print("Server closed")
                return
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
            if self.signals['shutdown']:
                print("Server closed")
                return
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'call_trump',
                'response': ans
            })

        def goAlone():
            ans = input('Go alone? y/n\n')
            if self.signals['shutdown']:
                print("Server closed")
                return
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

            if self.signals['shutdown']:
                print("Server closed")
                return
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'play_card',
                'response': ans
            })

        def discardCard():
            # Add top card to the hand
            hand = self.game_info['hand']
            top_card = self.game_info['top_card']
            hand.append(top_card)
            printCards(hand)

            # Get card to discard from user
            cards = [str(card) for card in hand]
            ans = input('Enter card to discard:\n')
            while ans not in cards:
                ans = input('Not a card in your hand.\n')

            # Remove and return discard card
            card_index = cards.index(ans)
            discard_card = hand.pop(card_index)

            if self.signals['shutdown']:
                print("Server closed")
                return
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'discard_card',
                'response': ans
            })

        request_options = {
            'order_up': orderUp,
            'order_trump': orderTrump,
            'call_trump': callTrump,
            'go_alone': goAlone,
            'play_card': playCard,
            'discard_card': discardCard,
        }

        request_options[request]()

    def decisionLoop(self, signals):
        """Wait for requests from server."""
        while not signals['shutdown']:
            time.sleep(0.1)
            if signals['request']:
                self.handleRequest(signals['request'])
                signals['request'] = None

    def heartbeat(self, signals):
        """Send UDP heartbeat message at regular intervals."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while not signals['shutdown']:
                sock.connect((self.socket_info['server_host'],
                              self.socket_info['server_hb_port']))
                message = json.dumps({
                    "message_type": "heartbeat",
                    "player_host": self.socket_info['host'],
                    "player_port": self.socket_info['port']
                })
                sock.sendall(message.encode('utf-8'))
                #print("Sent heartbeat")
                time.sleep(2)

    def sendMessage(self, message):
        """Send a TCP message to the server.

        Args:
            message (dict):
        """
        message['player_host'] = self.socket_info['host']
        message['player_port'] = self.socket_info['port']
        print("Message being sent:", message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.socket_info['server_host'],
                          self.socket_info['server_port']))
            message = json.dumps(message)
            sock.sendall(message.encode('utf-8'))

    def listen(self, signals):
        """Listen to a socket.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.setSocket(sock)
            self.listenLoop(sock, signals)

    def listenLoop(self, sock, signals):
        """Listen and handle messages over a TCP connection
        """
        while not signals["shutdown"]:
            message_dict = message_to_dictionary(sock)

            if message_dict == -1:
                continue

            print("Messaged recieved:", message_dict)

            # Networking functions
            # ------------------------------------------------------------------
            def handleRegisterAck():
                """Handle a registration acknowledgement.
                """
                hb_thread = threading.Thread(
                    target=self.heartbeat,
                    args=(signals,))
                hb_thread.start()
                self.threads.append(hb_thread)

            def handleShutdown():
                """Handle shutdown message.
                """
                self.signals['shutdown'] = True


            def serverTransfer():
                """Handle being transfered to a game server
                """
                self.socket_info['server_host'] = message_dict['new_host']
                self.socket_info['server_port'] = message_dict['new_port']
                self.socket_info['server_hb_port'] = message_dict['new_hb_port']
                self.registerWithServer()

            # Information updates that don't require a return value
            # ------------------------------------------------------------------

            def updateHandMsg():
                hand = message_dict['new_hand']
                self.game_info['hand'] = \
                    [Card.str2card(card) for card in hand]
                self.game_info['played_cards'] = []

            def pointsMsg():
                team1 = message_dict['team1']
                team2 = message_dict['team2']
                print()
                print(f"{team1['players'][0]}, {team1['players'][1]} have "
                      f"{team1['points']}\t{team2['players'][0]}, "
                      f"{team2['players'][1]} have {team2['points']}")
                print('-'*50)

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
                top_card = Card.str2card(message_dict['top_card'])
                self.game_info['top_card'] = top_card
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
                    f"{player} reneged by playing {card}")

            def invalidSuitMsg():
                print(
                    "Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")

            def trickStartMsg():
                print()

            def newTrumpMsg():
                self.game_info['trump'] = message_dict['trump']
                #print(f"The trump is {self.game_info['trump']}")

            def takerMsg():
                print(f"{message_dict['taker']} takes the trick")

            def roundResultsMsg():
                winners = message_dict['winners']
                points_scored = message_dict['points_scored']
                team_tricks = message_dict['tricks_taken']
                print("{} and {} win the round with {} point(s) and {} tricks taken"
                      .format(winners[0], winners[1],
                              points_scored, team_tricks))

            def gameResultsMsg():
                winners = message_dict['winners']
                print(f"{winners[0]} and {winners[1]} win the game!")

            # Handle the message
            # ------------------------------------------------------------------

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
                'round_results': roundResultsMsg,
                'game_results': gameResultsMsg,
            }

            networking_options = {
                'server_transfer': serverTransfer,
                'register_ack': handleRegisterAck,
                'shutdown': handleShutdown
            }
            # print("Message from server:", message_dict)

            if message_dict['message_type'] == 'info':
                info_options[message_dict['info_type']]()
            elif message_dict['message_type'] == 'request':
                signals['request'] = message_dict['request_type']
            elif message_dict['message_type'] == 'register_ack':
                networking_options['register_ack']()
            elif message_dict['message_type'] == 'server_transfer':
                networking_options['server_transfer']()
            elif message_dict['message_type'] == 'shutdown':
                networking_options['shutdown']()

    def setSocket(self, sock):
        """Bind the socket to the client.
        """
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.socket_info["host"], self.socket_info["port"]))

        # Set host and port in event that either was '' or 0
        self.socket_info["host"] = sock.getsockname()[0]
        self.socket_info["port"] = sock.getsockname()[1]

        sock.listen()
        sock.settimeout(1)


@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=0)
@click.option("--server-host", "server_host", default="localhost")
@click.option("--server-port", "server_port", default=6000)
@click.option("--server-hb-port", "server_hb_port", default=5999)
@click.option("--name", "name", default="WebConsole")
def main(host, port, server_host, server_port, server_hb_port, name):
    WebConsole(host, port, server_host, server_port, server_hb_port, name)


if __name__ == "__main__":
    main()
