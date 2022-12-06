import unittest
import filecmp
import os
import json
from pathlib import Path

import euchre
from euchre.players import ConsolePlayer 
from euchre.games import StandardGame
from euchre.players import TestPlayer
from euchre import Team

class TestGame(unittest.TestCase):

    debug = False
    logs = Path(__file__).parent / "logs/"

    # Clean up tmp directory for logs created during testing
    for f in os.listdir(logs / 'tmp'):
        os.remove(logs / 'tmp' / f)


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
        """
        Test that a misdeal occurs when everyone passes ordering up
        and ordering trump
        """

        # Paths to logs
        log_correct = self.logs / "correct/misdeal.log"
        log_test = self.logs / "tmp/misdeal.log"

        # Create game
        game = StandardGame(self.team1, self.team2, log_file=log_test,
                            shuffle=False, debug=False, round_count=1)

        # All players deny ordering up and ordering trump
        self.p3.commands = ['n', 'n']
        self.p2.commands = ['n', 'n']
        self.p4.commands = ['n', 'n']
        self.p1.commands = ['n', 'n']

        # Play games
        game.play()

        # Assert correct and new log are identical
        self.assertTrue(filecmp.cmp(log_correct, log_test))

    def test_passing(self):
        pass
   
    def test_taking(self):
        pass

    def test_reneging(self):
        pass
    
    def test_scoring_makers_win(self):
        """
        Test makers winning with 3 tricks and getting 1 point.
        """
        # Paths to logs
        log_correct = self.logs / "correct/maker_wins.log"
        log_test = self.logs / "tmp/maker_wins.log"

        # Create game
        game = StandardGame(self.team1, self.team2, log_file=log_test,
                            shuffle=False, deck_preset='balanced', debug=False,
                            round_count=1)

        # Using 'balanced' deck
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = ['n'           , '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = ['y', '1C', 'n', '1D', '1H', 'JS', '9S', '9H']

        # Play 1 round of the game
        game.play()

        # Load in points from game
        with open(log_correct) as f:
            correct = json.load(f)
        with open(log_test) as f:
            test = json.load(f)

        # Check points from correct and test log
        self.assertEqual(correct['points'], test['points'])

def test_scoring_makers_march(self):
    """
    Test makers winning with 5 tricks and getting 2 points.
    """
    pass

def test_scoring_maker_alone_win(self):
    """
    Test maker going alone and winning with 3 tricks for 1 point.
    """
    pass

def test_scoring_maker_alone_march(self):
    """
    Test maker going alone and winning with 5 tricks for 4 points.
    """
    pass

def test_scoring_defenders_win(self):
    """
    Test defenders winning with 3 tricks getting 2 points.
    """
    # TODO
    # TODO
    # TODO
    # Paths to logs
    log_correct = self.logs / "correct/maker_wins.log"
    log_test = self.logs / "tmp/maker_wins.log"

    # Create game
    game = StandardGame(self.team1, self.team2, log_file=log_test,
                        shuffle=False, deck_preset='balanced', debug=False,
                        round_count=1)

    # Using 'balanced' deck
    self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
    self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
    self.p4.commands = ['n'           , '9D', 'AH', 'KS', '9C', '1S']
    self.p1.commands = ['y', '1C', 'n', '1D', '1H', 'JS', '9S', '9H']

    # Play 1 round of the game
    game.play()

    # Load in points from game
    with open(log_correct) as f:
        correct = json.load(f)
    with open(log_test) as f:
        test = json.load(f)

    # Check points from correct and test log
    self.assertEqual(correct['points'], test['points'])
