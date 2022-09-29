import euchre

def play():
    """Play a singleplayer game of euchre in the console
    """
    p1 = euchre.ConsolePlayer('User')
    ai = []
    for i in range(3):
        ai.append(euchre.BasicAIPlayer('AI' + str(i)))
    team1 = euchre.Team(p1, ai[0])
    team2 = euchre.Team(ai[1], ai[2])
    game = euchre.StandardGame(team1, team2)
    game.play()

def connect(host='localhost', port=6001, server_host='localhost',
        server_port=6000, server_hb_port=5999):
    """Connect and play a web game of euchre in the console
    """
    euchre.clients.WebConsole(host, port, server_host, server_port,
            server_hb_port)
