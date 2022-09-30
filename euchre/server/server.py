"""Server class for managing Euchre games.
"""
import json
import subprocess
import threading
import socket
import click
import time

from euchre.players import WebPlayer
from euchre.players import BasicAIPlayer
from euchre.utils import message_to_dictionary
from euchre.players import Team
from euchre.games import StandardGame


class GameServer:
    """Server that runs games of euchre.

    Attributes:
        socket_info (dict):
            'host' (str): Hosting port of the server
            'port' (int): Port of this server
            'hb_port' (int): Port for heartbeats sent to this server
        signals (dict):
            'shutdown' (bool): True when server is shutting down,
                    otherwise False. Passed to looping functions
                    so they don't block
        local_players (list): Local Players
        online_players (dict): String addresses of web connected players
                    their Player object
        threads (list): Threads for asynchronous functions of the server
        player_count (int): Number of players in an online lobby, rest filled
                    mapped to with AI
    """

    def __init__(self, host, port, hb_port, player_count):
        self.socket_info = {
            'host': host,
            'port': int(port),
            'hb_port': int(hb_port)
        }
        self.player_count = player_count
        # Could this just be the gamestate, and is passed to all player classes?
        self.signals = {'shutdown': False,
                        'game_state': 'not_full'}  # 'not_full', 'full', 'playing', 'disconnect'

        # {self.host + ":" + str(self.port) : WebPlayer
        self.local_players = []
        self.online_players = dict()

        # Start threads
        self.threads = []
        self.startThreads(self.threads)

    def startThreads(self, threads):
        """Create threads for TCP and UDP connections.

        Creates a listening thread for TCP connections, a listening thread for
        UDP heartbeat connections, and a computational thread for checking
        the time deltas for client heartbeats.

        Args:
            threads (list): List to store threads for future use
        """
        # Make listening thread for heartbeat UDP connections
        hb_thread = threading.Thread(
            target=self.listenHeartbeat,
            args=(self.signals,))
        hb_thread.start()
        threads.append(hb_thread)

        # Make listening thread for TCP connections
        listen_thread = threading.Thread(
            target=self.listen,
            args=(self.signals,))
        listen_thread.start()
        threads.append(listen_thread)

        # Make heartbeat checking thread
        hb_ck_thread = threading.Thread(
            target=self.checkHeartbeat,
            args=(self.signals,))
        hb_ck_thread.start()
        threads.append(hb_ck_thread)

    def shutdown(self):
        """Shuts down the server.
        """
        # The signal is in the while loop of every thread, when it is false
        #   all loops will terminate and threads join
        for player in self.online_players.values():
            message = {'message_type': 'shutdown'}
            player.sendMessage(message)
            # print(player.address)
        time.sleep(100)

        self.signals['shutdown'] = True
        # time.sleep(1)
        # for thread in self.threads:
        #     thread.join()

    def checkHeartbeat(self, signals):
        """Check client heartbeats.

        Args:
            signals (dict):
                'shutdown' (bool): True when the server is shutting down and
                    threads need to be joined
        """
        while not signals["shutdown"]:

            # Check if each player missed a heartbeat
            for player in self.online_players.values():
                if time.perf_counter() - player.last_heartbeat >= 10:
                    print(player, "missed a heartbeat")
                    pass
            time.sleep(2)

    def listenHeartbeat(self, signals):
        """Listen for UDP heartbeat messages from players.

        Args:
            signals (dict):
                'shutdown' (bool): True when the server is shutting down and
                    threads need to be joined
        """
        # Connect to socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.socket_info["host"], self.socket_info["hb_port"]))
            sock.settimeout(1)

            # Listen for UDP heartbeat messages until shutdown signal
            while not signals["shutdown"]:
                try:
                    message_bytes = sock.recv(4096)
                except socket.timeout:
                    continue
                message_str = message_bytes.decode("utf-8")
                message_dict = json.loads(message_str)
                address = WebPlayer.getAddress(message_dict["player_host"],
                                               message_dict["player_port"])
                player = self.online_players[address]
                player.last_heartbeat = time.perf_counter()
                # print("Recieved heartbeat")

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

            def handleRegister():
                """Handle web players registering.
                """
                #print("Registering player...")
                if len(self.online_players) + len(self.local_players) >= 4:
                    print("Error: Too many players registered")
                    return
                #print(message_dict)
                web_player = WebPlayer(message_dict['player_host'],
                                       message_dict['player_port'],
                                       message_dict['player_name'])
                self.online_players[web_player.address] = web_player

                # Send TCP acknowledgement to web player
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((web_player.host, web_player.port))
                    message = json.dumps({
                        'message_type': 'register_ack',
                        'player_host': web_player.host,
                        'player_port': web_player.port
                    })
                    sock.sendall(message.encode('utf-8'))
                print("Player", web_player, "registered")

                if len(self.online_players) != self.player_count:
                    slots_avail = self.player_count - len(self.online_players)
                    print(f"Waiting for {slots_avail} player(s)")

            def webPlayerMsg():
                """Handle a message from a web player.
                """
                player_host = message_dict['player_host']
                player_port = message_dict['player_port']
                address = WebPlayer.getAddress(player_host, player_port)
                self.online_players[address].recvMessage(message_dict)

            def handleShutdown():
                """Shut down the server
                """
                self.shutdown()

            options = {
                'register': handleRegister,
                'response': webPlayerMsg,
                'shutdown': handleShutdown
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
        sock.listen()
        sock.settimeout(1)

    def getPlayer(self, host, port):
        """Return the player object given a unique host and port.
        """
        address = PlayerInfo.get_address(host, port)
        return self.players[address]

    def playGame(self, player_count=1):
        """Play a game of euchre online.

        Waits for an online client to join then starts the game.
        """
        while len(self.online_players) != player_count:
            time.sleep(1)
        players = list(self.online_players.values())
        for i in range(4 - player_count):
            players.append(BasicAIPlayer('AI' + str(i)))
        team1 = Team(players[0], players[1])
        team2 = Team(players[2], players[3])
        game = StandardGame(team1, team2)

        print("starting game...")
        game.play()


@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=6000)
@click.option("--hb-port", "hb_port", default=5999)
@click.option("--player-count", "player_count", default=4)
def main(host, port, hb_port, player_count):
    server = GameServer(host, port, hb_port, player_count)
    server.playGame(player_count)


if __name__ == '__main__':
    main()
