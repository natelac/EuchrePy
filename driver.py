from consoleplayer import HumanPlayer
from basicai import BasicAIPlayer
from team import Team
from standardgame import StandardGame

p1 = HumanPlayer('User')
ai = []
for i in range(3):
    ai.append(BasicAIPlayer('AI' + str(i)))
team1 = Team(p1, ai[0])
team2 = Team(ai[1], ai[2])
game = StandardGame(team1, team2)
game.play()
