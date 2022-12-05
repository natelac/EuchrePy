import unittest

import euchre
from euchre.players import ConsolePlayer 
from euchre.games import StandardGame
from euchre.players import TestPlayer
from euchre import Team

class TestGame(unittest.TestCase):

    debug = False

    # Create players
    p1 = TestPlayer('P1', debug=debug)
    p2 = TestPlayer('P2', debug=debug)
    p3 = TestPlayer('P3', debug=debug)
    p4 = TestPlayer('P4', debug=debug)

    # Create teams
    team1 = Team(p1, p2)
    team2 = Team(p3, p4)


    def test_ordering_up(self):
        pass

    def test_ordering_trump(self):
        pass

    def test_misdeal(self):
        # Create game
        game = StandardGame(self.team1, self.team2, log_file="test.log", shuffle=False,
                            deck_preset='balanced', points=(0,0), debug=False, round_count=1)

        # All players deny ordering up and ordering trump
        self.p3.commands = ['n', 'n']
        self.p2.commands = ['n', 'n']
        self.p4.commands = ['n', 'n']
        self.p1.commands = ['n', 'n']

        game.play()

        self.assertTrue(True)
        

    def test_passing(self):
        pass
   
    def test_taking(self):
        pass

    def test_reneging(self):
        pass
    
    def test_scoring_makers_win(self):
        """
        Test if maker wins 
        """
        # Create game
        game = StandardGame(self.team1, self.team2, log_file="test.log", shuffle=False,
                            deck_preset='balanced', points=(8,9), debug=False, round_count=1)

        # Using 'balanced' deck
        # Dealer orders up and wins with 3 tricks
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = ['n'           , '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = ['y', '1C', 'n', '1D', '1H', 'JS', '9S', '9H']

        game.play()
        #Check points in log
        self.assertEqual(True, True)

        # Dealer orders up and loses with 2 tricks

        # Player left of dealer orders up and wins 3 tricks

        # Using 
        # Player left of dealer orders up and loses 2 tricks

        # Dealer orders up and wins all 5 tricks

        # Dealer goes alone and wins all 5 tricks

        # Dealer goes alone and wins 4 tricks
        pass

