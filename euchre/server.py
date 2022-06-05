"""Server class for managing Euchre games"""
import json
import subprocess
import threading
import socket
import click
import time
#from players.online.webplayer import WebPlayer
from euchre.players import WebPlayer
from euchre.players import BasicAIPlayer
from euchre.utils import message_to_dictionary
from euchre.players import Team
from euchre.games import StandardGame


class GameServer:
    def __init__(self, host, port, hb_port):
        self.socket_info = {
            'host': host,
            'port': int(port),
            'hb_port': int(hb_port)
        }
        # Could this just be the gamestate, and is passed to all player classes?
        self.signals = {'shutdown': False,
                        'game_state': 'not_full'} # 'not_full', 'full', 'playing', 'disconnect'

        # {self.host + ":" + str(self.port) : PlayerInfo(host, port)
        self.local_players = []
        self.online_players = {}

        #
        self.threads = []
        self.startThreads()

    def startThreads(self):
        # Make heartbeat thread for UDP connections
        hb_thread = threading.Thread(
                target=self.listenHeartbeat,
                args=(self.signals,))
        hb_thread.start()
        self.threads.append(hb_thread)

        # Make heartbeat checking thread
        hb_ck_thread = threading.Thread(
                target=self.checkHeartbeat,
                args=(self.signals,))
        hb_ck_thread.start()
        self.threads.append(hb_ck_thread)

        # Make listening thread for TCP connections
        listen_thread = threading.Thread(
                target=self.listen,
                args=(self.signals,))
        listen_thread.start()
        self.threads.append(listen_thread)

    def shutdown(self):
        self.signals['shutdown'] = True # Will cause heartbeat threads to shutdown
        #TODO
        ## You probabably need to tell clients server is shutting down
        # Send shutdown message to workers
        # for worker in self.workers.values():
        #     if worker.status != Worker.Status.DEAD:
        #         message = {"message_type": "shutdown"}
        #         worker.send_message(message)

        # terminate the server itself
        self.signals['shutdown'] = True
        for thread in self.threads:
            thread.join()

    def checkHeartbeat(self, signals):
        """Check worker hearbeat messages"""
        while not signals["shutdown"]:
            for player in self.online_players.values():
                if time.perf_counter() - player.last_heartbeat >= 10:
                    pass
                    #print(player, "missed a heartbeat")
            time.sleep(2)

    def listenHeartbeat(self, signals):
        """Listen for UDP hearbeat messages from players."""
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
                worker = self.getPlayer(message_dict["player_host"],
                                         message_dict["player_port"])
                worker.last_heartbeat = time.perf_counter()

    def listen(self, signals):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.setSocket(sock)
            self.listenLoop(sock, signals)

    def listenLoop(self, sock, signals):
        """Loop for listen."""
        print("Server listening for registers...")
        while not signals['shutdown']:
            message_dict = message_to_dictionary(sock)

            def handleRegister():
                """Handle register."""
                print("Registering player...")
                if len(self.online_players) + len(self.local_players)  >= 4:
                    print("Error: Too many players registered")
                    return

                web_player = WebPlayer(message_dict['player_host'],
                                        message_dict['player_port'])
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

                #TODO
                #   - If full with 4 players, change game_state to ready,
                #       call a function for playing the game
                print("Player", web_player, "registered")

            def webPlayerMsg():
                player_host = message_dict['player_host']
                player_port = message_dict['player_port']
                address = WebPlayer.getAddress(player_host, player_port)
                self.online_players[address].recvMessage(message_dict)

            options = {
                        'register': handleRegister,
                        'response': webPlayerMsg
                        # 'shutdown': handleShutdown
                      }

            # Execute handle message based on type
            if message_dict == -1:
                continue
            print("Message recieved:", message_dict)
            options[message_dict['message_type']]()

    def setSocket(self, sock):
        """Bind the socket to the server."""
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.socket_info["host"], self.socket_info["port"]))
        sock.listen()
        sock.settimeout(1)

    def getPlayer(self, host, port):
        """Return the player object given a unique host and port."""
        address = PlayerInfo.get_address(host, port)
        return self.players[address]

    def playGame(self):
        #TODO
        while len(self.online_players) == 0:
            time.sleep(1)
        p1 = list(self.online_players.values())[0]
        ai = []
        for i in range(3):
            ai.append(BasicAIPlayer('AI' + str(i)))
        team1 = Team(p1, ai[0])
        team2 = Team(ai[1], ai[2])
        game = StandardGame(team1, team2)
        game.play()

@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=6000)
@click.option("--hb-port", "hb_port", default=5999)
def main(host, port, hb_port):
    server = GameServer(host, port, hb_port)
    server.playGame()

if __name__ == '__main__':
    main()
