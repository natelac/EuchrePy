from euchre.players import TestPlayer
from euchre.players import ConsolePlayer
from euchre import Team
from euchre import StandardGame
from euchre import Deck

# Create players
p1 = TestPlayer('P1', debug=True)
p2 = TestPlayer('P2', debug=True)
p3 = TestPlayer('P3', debug=True)
p4 = TestPlayer('P4', debug=True)

# Create teams
team1 = Team(p1, p2)
team2 = Team(p3, p4)

# Create game 
game = StandardGame(team1, team2, log_file="test.log", shuffle=False, 
                    deck_preset='balanced', points=(9,8), debug=True)

# Tests
# p1 is the dealer
p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
p4.commands = ['n'           , '9D', 'AH', 'KS', '9C', '1S']
p1.commands = ['y', '1C', 'n', '1D', '1H', 'JS', '9S', '9H']

game.play()
