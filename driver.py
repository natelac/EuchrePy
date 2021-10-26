from consoleplayer import HumanPlayer
from basicai import BasicAIPlayer
from _team import Team
from _standardgame import StandardGame

'''
TODO:
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

- Short term
    - First to 10 declared winner
    - Reneging

- Medium Term
    - Going alone
    - messaging to player for if they get reneged, telling them what happens
    AFTER they play there card (rather than globally printing)

- Once fundemental game works:
    - Clean up code,
    - organize methods,
    - create doc strings
    - DisplayAscii() function for Card() to be used in consoleplayer
        - Colored emojis for suits and ranks
    - Make Euchre() class as driver instead

- Long Term
    - APIPlayer for interfacing with a webapp through javascript
    - Create a Game Class that can be extended to create variations of euchre
    - MLPlayer that makes decisions from a trained ML/ interfaces with one
    to train it? Along with a driver class that will train the network by
    running through the game?
'''



p1 = HumanPlayer('User')
ai = []
for i in range(3):
    ai.append(BasicAIPlayer('AI' + str(i)))
team1 = Team(p1, ai[0])
team2 = Team(ai[1],ai[2])
game = StandardGame(team1,team2)
game.play()
