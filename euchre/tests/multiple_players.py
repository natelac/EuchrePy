from euchre.players import ConsolePlayer
from euchre import Team
from euchre import StandardGame
from euchre import Deck

# Create players
p1 = ConsolePlayer('P1')
p2 = ConsolePlayer('P2')
p3 = ConsolePlayer('P3')
p4 = ConsolePlayer('P4')

# Create teams
t1 = Team(p1, p2)
t2 = Team(p3, p4)

# Disable shuffling for testing
Deck.disable_shuffle = True

# Play the game
game = StandardGame(t1, t2)
game.play()
