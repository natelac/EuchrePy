from consoleplayer import HumanPlayer
from basicai import BasicAIPlayer
from _team import Team
from _standardgame import StandardGame

'''
- How to implment scoring:
    - Play through all five tricks first
    - Check that each player played every card in there hand (and nothing new)
    - validate that each play was valid
        - Create a method that checks which cards in hand were valid to play.
            Perform a simple "was card played in valid cards", unless there were
            no valid cards, then return True
        - Start from front playing cards that player played.

- Have taker and trick saved in StandardGame (and reset where appropriate)
  - Instead pass game object to player?
      - You might want to eventually create a Game superclass and have
          StandardGame extend it
'''



p1 = HumanPlayer('User')
ai = []
for i in range(3):
    ai.append(BasicAIPlayer('AI' + str(i)))
team1 = Team(p1, ai[0])
team2 = Team(ai[1],ai[2])
game = StandardGame(team1,team2)
game.play()
