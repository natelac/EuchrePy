import euchre

p1 = euchre.players.ConsolePlayer('User')
ai = []
for i in range(3):
    ai.append(euchre.players.BasicAIPlayer('AI' + str(i)))
team1 = euchre.Team(p1, ai[0])
team2 = euchre.Team(ai[1], ai[2])
game = euchre.StandardGame(team1, team2)
game.play()
