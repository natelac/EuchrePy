import unittest

import euchre
from euchre.players import ConsolePlayer 
from euchre.games import StandardGame


class test_game(unittest.Testcase):

    # Create players
    p1 = ConsolePlayer('P1')
    p2 = ConsolePlayer('P2')
    p3 = ConsolePlayer('P3')
    p4 = ConsolePlayer('P4')

    def test_ordering_up(self):
        pass

    def test_ordering_trump(self):
        pass

    def test_misdeal(self):
        pass

    def test_passing(self):
        pass
   
    def test_taking(self):
        pass

    def test_reneging(self):
        pass
    
    def test_scoring(self):
        pass
