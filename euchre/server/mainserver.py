
"""Server class for connecting players to games.
"""
import json
import subprocess
import threading
import socket
import click
import time
from multiprocessing import Process, Value
from ctypes import c_wchar_p

from euchre.players import WebPlayer
from euchre.players import BasicAIPlayer
from euchre.utils import message_to_dictionary
from euchre.players import Team
from euchre.games import StandardGame
from euchre.server import GameServer


class MainServer:
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
        game_servers (list):
            (dict):
                'host' (str): Address of the game server
                'port' (str): Port of the game server
                'hb_port' (str): Port for heartbeats sent to the game server
                'is_full' (multiprocessing.Value): Whether game server is full, or can take more players
    """

    def __init__(self, host, port, player_count):
        self.socket_info = {
            'host': host,
            'port': int(port),
        }
        self.player_count = player_count
        self.signals = {'shutdown': False}

        # Start threads
        self.threads = []
        self.startThreads(self.threads)

        # Value in shared memory between all servers
        self.shutdown_games = Value('b', True)

        # List of dictionaries containing game server information
        self.game_servers = []
        self.game_processes = []

        self.makeGameServer()

    def makeGameServer(self):
        """Start new game server for players.
        """
        # Method for starting up a new game server
        def spawnGameServer(self, *args):
            # print(args)
            server = GameServer(*args)

        # Create shared server information
        # host is actually not mutable since it is a pointer
        shared_info = {
                'server_full': Value('b', False),
                'host': Value(c_wchar_p, self.socket_info['host']),
                'port': Value('i', 0),
                'hb_port': Value('i', 0),
                }
        self.game_servers.append(shared_info)

        # Start game server on another process
        p = Process(target=spawnGameServer, args=(self,
                self.shutdown_games, shared_info, 
                self.player_count))
        p.start()
        self.game_processes.append(p)

        return shared_info

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
        print("main server listening for registers...")
        while not signals['shutdown']:
            message_dict = message_to_dictionary(sock)

            # Debugging
            # print('server_full', self.game_servers[0]['server_full'].value)
            # print('port', self.game_servers[0]['port'].value)
            # print('hb_port', self.game_servers[0]['hb_port'].value)

            # Skip if no message
            if message_dict == -1:
                continue

            def transferPlayer():
                """Handle web players trying to register with main server
                """

                # Gets available server by finding one or making one
                server_info = self.getAvailableServer()

                # Wait up to 1 second for the game servers socket to set
                count = 0
                while server_info['port'].value == 0 and count < 10:
                    time.sleep(0.1)
                    count += 1

                # print(message_dict['player_host'])
                # print(message_dict['player_port'])

                # Send address of new server to player
                # We use port of this server since it is the same, (and some
                # finicky issues with c pointers)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((message_dict['player_host'], 
                                  message_dict['player_port']))
                    message = json.dumps({
                        'message_type': 'server_transfer',
                        'new_host': self.socket_info['host'],
                        'new_port': server_info['port'].value,
                        'new_hb_port': server_info['hb_port'].value,
                    })
                    sock.sendall(message.encode('utf-8'))
                print("Player", message_dict['player_name'], 
                      "transfered to game server with port", 
                      server_info['port'].value)

            options = {
                'register': transferPlayer,
                'shutdown': self.shutdown
            }

            # Handle the recieved message
            options[message_dict['message_type']]()

    def getAvailableServer(self):
        """Gets server information to transfer a user to, creates one if
        it does not exist.
        """
        # Return first empty server found
        for server_info in self.game_servers[::-1]:
            if server_info['server_full'].value == False:
                return server_info

        # Otherwise return a new server 
        server_info = self.makeGameServer()
        return server_info


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
@click.option("--player-count", "player_count", default=4)
def main(host, port, player_count):
    server = MainServer(host, port, player_count)


if __name__ == '__main__':
    main()
