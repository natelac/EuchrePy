import euchre


def play():
    """Play a singleplayer game of euchre in the console
    """
    p1 = euchre.players.ConsolePlayer('User')
    ai = []
    for i in range(3):
        ai.append(euchre.players.BasicAIPlayer('AI' + str(i)))
    team1 = euchre.players.Team(p1, ai[0])
    team2 = euchre.players.Team(ai[1], ai[2])
    game = euchre.games.StandardGame(team1, team2)
    game.play()


def connect(host='localhost', port=0, server_host='localhost',
            server_port=6000, server_hb_port=5999, name='WebConsole'):
    """Connect and play a web game of euchre in the console
    """
    euchre.clients.WebConsole(host, port, server_host, server_port,
                              server_hb_port, name)
