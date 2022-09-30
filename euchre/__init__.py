"""An extendible package for playing euchre locally and hosting and playing
games of euchre online.
"""
from euchre import games
from euchre import players
from euchre import clients
from euchre import server
from euchre.games import StandardGame
from euchre.players import Player
from euchre.players import Team
from euchre.players import BasicAIPlayer
from euchre.players import ConsolePlayer
from euchre.players import WebPlayer
from euchre.cards import Card
from euchre.cards import Deck
from euchre.play import play
from euchre.play import connect
