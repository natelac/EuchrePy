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
    create_correct_logs = False
    logs = Path(__file__).parent / "logs/"
    
    # Create new logs to check test logs against,
    # always check the correct logs to make sure they are actually correct
    if create_correct_logs:
        for f in os.listdir(logs / 'correct'):
            os.remove(logs / 'correct' / f)

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
        # Paths to logs
        log_correct = self.logs / "correct/ordering_up.log"
        log_test = self.logs / "tmp/ordering_up.log"
        if self.create_correct_logs:
            log_test = log_correct

        # Create game
        game = StandardGame(self.team1, self.team2, log_file=log_test,
                            shuffle=False, deck_preset='balanced', 
                            debug=self.debug, round_count=1, points=(0,0))

        # Test p3 ordering up
        self.p3.commands = ['y',         'n', 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = [                 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = [                 '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = [            '1D','9S', '1H', 'JS', '1C', '9H']
        game.play()

        # Test p2 ordering up
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['y',       'n', 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = [                '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = [          '1D', '9S', '1H', 'JS', '1C', '9H']
        game.play()

        # Test p4 ordering up
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = ['y'        'n', '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = [          '1D', '9S', '1H', 'JS', '1C', '9H']
        game.play()

        # Test p1 ordering up
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = ['n'           , '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = ['y', '1D', 'n', '9S', '1H', 'JS', '1C', '9H']
        game.play()

        # Load in log of game
        # TODO: Load in test in line by line
        # with open(log_correct) as f:
            # correct = json.load(f)
        with open(log_test) as f:
            test = json.load(f)
        print(correct)


    def test_ordering_trump(self):
        pass

    def test_misdeal(self):
        """
        Test that a misdeal occurs when everyone passes ordering up
        and ordering trump.
        """

        # Paths to logs
        log_correct = self.logs / "correct/misdeal.log"
        log_test = self.logs / "tmp/misdeal.log"
        if self.create_correct_logs:
            log_test = log_correct

        # Create game
        game = StandardGame(self.team1, self.team2, log_file=log_test,
                            shuffle=False, debug=self.debug, round_count=1,
                            points=(0,0))

        # All players deny ordering up and ordering trump
        self.p3.commands = ['n', 'n']
        self.p2.commands = ['n', 'n']
        self.p4.commands = ['n', 'n']
        self.p1.commands = ['n', 'n']

        # Play games
        game.play()

        # Assert correct and new log are identical
        # this could also just check that the file reads "Misdeal"
        self.assertTrue(filecmp.cmp(log_correct, log_test))

    def test_reneging(self):
        pass
    
    def test_scoring_makers_win(self):
        """
        Test makers winning with 3 tricks and getting 1 point.
        """
        # Paths to logs
        log_correct = self.logs / "correct/makers_win.log"
        log_test = self.logs / "tmp/makers_win.log"
        if self.create_correct_logs:
            log_test = log_correct

        # Create game
        game = StandardGame(self.team1, self.team2, log_file=log_test,
                            shuffle=False, deck_preset='balanced', 
                            debug=self.debug, round_count=1, points=(0,0))

        # Using 'balanced' deck
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = ['n'           , '9D', 'AH', 'KS', '9C', '1S']
        self.p1.commands = ['y', '1D', 'n', '9S', '1H', 'JS', '1C', '9H']

        # Play 1 round of the game
        game.play()

        # Load in points from game
        with open(log_correct) as f:
            correct = json.load(f)
        with open(log_test) as f:
            test = json.load(f)

        # Check that team1 (team of makers) get 1 point
        self.assertEqual(test['points'], [1,0])

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
        # Paths to logs
        log_correct = self.logs / "correct/defenders_win.log"
        log_test = self.logs / "tmp/defenders_win.log"
        if self.create_correct_logs:
            log_test = log_correct

        # Create game
        game = StandardGame(self.team1, self.team2, log_file=log_test,
                            shuffle=False, deck_preset='balanced', 
                            debug=self.debug, round_count=1, points=(0,0))

        # Using 'balanced' deck
        self.p3.commands = ['n'           , 'AD', 'QH', 'JC', 'QC', 'KD']
        self.p2.commands = ['n'           , 'QD', 'KH', 'AS', 'AC', 'KC']
        self.p4.commands = ['n'           , '9D', 'AH', 'KS', '1S', '9C']
        self.p1.commands = ['y', '1C', 'n', '1D', '1H', 'JS', '9S', '9H']

        # Play 1 round of the game
        game.play()

        # Load in points from game
        with open(log_correct) as f:
            correct = json.load(f)
        with open(log_test) as f:
            test = json.load(f)

        # Check that team2 (team of defenders) get 2 points
        self.assertEqual(test['points'], [0, 2])
