
"""Server class for connecting players to games.
"""
import json
import subprocess
import threading
import socket
import click
import time
from multiprocessing import Process, Value

from euchre.players import WebPlayer
from euchre.players import BasicAIPlayer
from euchre.utils import message_to_dictionary
from euchre.players import Team
from euchre.games import StandardGame
from euchre.server import GameServer


class MasterServer:
    """Server class for connecting players to games.

    Recieves messages from players and refers them to a game server. 
    Spawns new game servers when they become full. Because of the Python GIL,
    we use the multiprocessing module to create new game servers.

    Attributes:
        socket_info (dict):
            'host' (str): Address of the server
            'port' (int): Port of this server
        signals (dict):
            'shutdown' (bool): True when server is shutting down,
                    otherwise False. Passed to looping functions
                    so they don't block
        threads (list): Threads for asynchronous functions of the server
        game_servers (dict):
            'host' (str): Address of the game server
            'port' (str): Port of the game server
            'hb_port' (str): Port for heartbeats sent to the game server
            'is_full' (multiprocessing.Value): Whether game server is full, or can take more players
    """

    def __init__(self, host, port, hb_port, player_count):
        self.socket_info = {
            'host': host,
            'port': int(port),
            'hb_port': int(hb_port)
        }
        self.player_count = player_count
        self.signals = {'shutdown': False}

        # Start threads
        self.threads = []
        self.startThreads(self.threads)

        # Not a bool but we can treat it like one
        self.shutdown_games = Value('b', True)
        self.game_processes = []

    def makeGameServer(self):

        # Function for starting up a new game server
        def spawnGameServer(self):
            server = GameServer()
            server.playGame(self.player_count)

        # Start game server on another process
        p = Process(target=spawnGameServer, args=(
                self.shutdown_games, self.socket_info['host'], 0, 0, 
                self.player_count))
        p.start()
        self.game_processes.append(p)

    def startThreads(self, threads):
        """Starts TCP listening thread.
        Args:
            threads (list): List to store threads for future use
        """
        # Make listening thread for TCP connections
        listen_thread = threading.Thread(
            target=self.listen,
            args=(self.signals,))
        listen_thread.start()
        threads.append(listen_thread)

    def shutdown(self):
        """Shuts down the server.
        """
        # The signal is in the while loop of every thread, when it is false
        # all loops will terminate and threads join
        for player in self.online_players.values():
            message = {'message_type': 'shutdown'}
            player.sendMessage(message)
        time.sleep(5)
        self.signals['shutdown'] = True
        self.shutdown_games.value = True
        time.sleep(5)
        for p in self.game_processes:
            p.join()


    def listen(self, signals):
        """Loop for listening to TCP connections

        Args:
            signals (dict):
                'shutdown' (bool): True when the server is shutting down and
                    threads need to be joined
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.setSocket(sock)
            self.listenLoop(sock, signals)

    def listenLoop(self, sock, signals):
        """Loop for listening to TCP connections.

        Handles players registering and recieving messages from web players.

        Args:
            sock (socket): Socket for TCP connections
            signals (dict):
                'shutdown' (bool): True when the server is shutting down and
                    threads need to be joined
        """
        print("server listening for registers...")
        while not signals['shutdown']:
            message_dict = message_to_dictionary(sock)

            def registerPlayer():
                """Handle web players registering.
                """
                web_player = WebPlayer(message_dict['player_host'],
                                       message_dict['player_port'],
                                       message_dict['player_name'])
                self.online_players[web_player.address] = web_player

                # Send TCP acknowledgement to web player
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((web_player.host, web_player.port))
                    message = json.dumps({
                        'message_type': 'register_ack',
                        'player_host': message_dict['player_host'],
                        'player_port': message_dict['player_port']
                    })
                    sock.sendall(message.encode('utf-8'))
                print("Player", web_player, "transfered to", )

            options = {
                'register': registerPlayer,
                'response': webPlayerMsg,
                'shutdown': self.shutdown
            }

            # Handle the recieved message
            if message_dict == -1:
                continue
            #print("Message recieved:", message_dict)
            options[message_dict['message_type']]()

    def setSocket(self, sock):
        """Bind the socket to the server.
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
@click.option("--port", "port", default=6000)
@click.option("--hb-port", "hb_port", default=5999)
@click.option("--player-count", "player_count", default=4)
def main(host, port, hb_port, player_count):
    server = MasterServer(host, port, hb_port, player_count)


if __name__ == '__main__':
    main()
