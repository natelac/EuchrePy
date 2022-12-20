
import socket
import json
import threading
import time
import click
import random

from euchre.utils import message_to_dictionary
from euchre.utils import printCards
from euchre.cards import Card

class WebAI:
    """An AI that plays euchre over the web.

    TODO:
        - All todos in WebConsole
        - Create a parent class for WebConsole and WebAI
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
            'cards_played': [],
            'lead_cards': []
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

        # print(self.socket_info['host'],
        #       self.socket_info['port'])
        self.registerWithServer() 

        # Halts this flow until listen_thread gets shutdown message
        listen_thread.join()
        decision_thread.join()

    # Imported methods
    # Maybe list out explicitily?
    # from ._requests import orderUp, orderTrump, callTrump, goAlone,
    #         play_card, discardCard

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

            if self.signals['shutdown']:
                return

            # Order up 25% of the time
            ans = 'y' if random.random() <= 0.25 else 'n'
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'order_up',
                'response': ans
            })

        def orderTrump():

            if self.signals['shutdown']:
                return

            # Order trump 25% of the time
            ans = 'y' if random.random() <= 0.25 else 'n'
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'order_trump',
                'response': ans
            })

        def callTrump():

            if self.signals['shutdown']:
                return

            # Pick a random suit that wasn't the top card suit
            suits = {'C', 'S', 'H', 'D'}
            valid_suits = suits - {self.game_info['top_card'].suit}
            ans = random.sample(list(valid_suits),1)
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'call_trump',
                'response': ans[0]
            })

        def goAlone():

            if self.signals['shutdown']:
                return

            # Go alone 5% of the time
            ans = 'y' if random.random() <= 0.05 else 'n'
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'go_alone',
                'response': ans
            })

        def playCard():

            if self.signals['shutdown']:
                return

            # Play an arbitrary valid card

            # Cards played so far by all players
            cards_played = self.game_info['cards_played'][-1]

            # Select card to play
            if len(cards_played) == 0:
                # Pick arbitrary card (top card) if this is the leading card
                card_to_play = self.game_info['hand'][0]
            else:
                # Otherwise pick first card that matches led suit
                led_suit = cards_played[0].suit
                card_to_play = None
                for card in self.game_info['hand']:
                    if card.getSuit(led_suit) == led_suit:
                       card_to_play = card 
                       break

                if card_to_play is None:
                    card_to_play = self.game_info['hand'][0]

            # Remove card from hand, add to playedCards
            self.game_info['hand'].remove(card_to_play)
            self.game_info['cards_played'][0].append(card_to_play)

            self.sendMessage({
                'message_type': 'response',
                'response_type': 'play_card',
                'response': str(card_to_play)
            })

        def discardCard():

            # Add top card to the hand
            discard_card = self.game_info['hand'].pop()
            self.game_info['hand'].append(self.game_info['top_card'])

            if self.signals['shutdown']:
                # print("Server closed")
                return
            self.sendMessage({
                'message_type': 'response',
                'response_type': 'discard_card',
                'response': str(discard_card)
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
                self.game_info['cards_played'] = []

            def pointsMsg():
                team1 = message_dict['team1']
                team2 = message_dict['team2']

            def dealerMsg():
                dealer = message_dict['dealer']

            def topCardMsg():
                top_card = message_dict['top_card']
                self.game_info['top_card'] = Card.str2card(top_card)

            def deniedUpMsg():
                denier = message_dict['denier']

            def orderedUpMsg():
                orderer = message_dict['orderer']
                top_card = Card.str2card(message_dict['top_card'])
                self.game_info['top_card'] = top_card

            def deniedTrumpMsg():
                denier = message_dict['denier']

            def orderedTrumpMsg():
                orderer = message_dict['orderer']
                trump_suit = message_dict['trump_suit']

            def misdealMsg():
                pass

            def leaderMsg():
                leader = message_dict['leader']

            def playedMsg():
                player = message_dict['player']
                card = Card.str2card(message_dict['card'])
                self.game_info['cards_played'][-1].append(card)

            def takerMsg():
                taker = message_dict['taker']

            def penaltyMsg():
                player = message_dict['player']
                card = message_dict['card']

            def invalidSuitMsg():
                pass

            def trickStartMsg():
                self.game_info['cards_played'].append([])
                pass

            def newTrumpMsg():
                self.game_info['trump'] = message_dict['trump']

            def takerMsg():
                pass

            def roundResultsMsg():
                winners = message_dict['winners']
                points_scored = message_dict['points_scored']
                team_tricks = message_dict['tricks_taken']

            def gameResultsMsg():
                winners = message_dict['winners']

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
    WebAI(host, port, server_host, server_port, server_hb_port, name)


if __name__ == "__main__":
    main()
