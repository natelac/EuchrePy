from euchre.players.local.consoleplayer import ConsolePlayer
from euchre.players.local.basicai import BasicAIPlayer
from euchre.players.team import Team
from euchre.games.standardgame import StandardGame

p1 = ConsolePlayer('User')
ai = []
for i in range(3):
    ai.append(BasicAIPlayer('AI' + str(i)))
team1 = Team(p1, ai[0])
team2 = Team(ai[1], ai[2])
game = StandardGame(team1, team2)
game.play()
