import abc
import itertools

from euchre.utils import printCards as utilPrintCards

class Player(abc.ABC):
    """Base Player class used in a Euchre game.

    Player objects are directly called by the game.

    Attributes:
        name: Name of the player
        team: Team that the player is on
        hand: List of cards in the players hand
    """
    id_iter = itertools.count()

    def __init__(self, name=''):
        self.id = next(Player.id_iter)
        self.name = name
        self.team = None
        self.hand = None
        self.game_info = {'trump_suit': None,
                          'leader': None,
                          'down_cards': None}
        self._playedCards = []

    def __str__(self):
        """Gets name of player"""
        return self.name

    def getTeammate(self):
        """Gets teammate

        Returns:
            Player that is on the same team as this Player."""
        return self.team.getTeammate(self)

    def printCards(self):
        """Prints 'nice' view of player's hand to console."""
        utilPrintCards(self.hand)

    # Decision methods that require a return value
    # ----------------------------------------------
    @abc.abstractmethod
    def orderUp(self):
        """Determines whether player will order up.

        Returns:
            True if player is ordering up, otherwise False.
        """
        pass

    @abc.abstractmethod
    def orderTrump(self):
        """Determines whether player will order trump.

        Returns:
            True if player is ordering trump, otherwise False.
        """
        pass

    @abc.abstractmethod
    def callTrump(self):
        """Gets players call for trump.

        Returns:
            Suit that player will call for trump.
        """
        pass

    @abc.abstractmethod
    def playCard(self):
        """Gets players card to be played during a trick.

        Returns:
            A card that player selects.
        """
        pass

    @abc.abstractmethod
    def goAlone(self):
        """Gets whether player is going alone.

        Returns:
            True if player is going alone, otherwise False.
        """
        pass

    @abc.abstractmethod
    def discardCard(self, top_card):
        """Called when this Player is orderd up, passes the top Card.

        Returns:
            Card to throw in kitty.
        """
        pass

    # Information updates that don't require a return value
    # -----------------------------------------------------
    @abc.abstractmethod
    def updateHand(self, cards):
        """Updates cards in players hand
        """
        pass

    @abc.abstractmethod
    def pointsMsg(self, team1, team2):
        """Passes Teams which contains the players on the team and the points
        the players have.

        For human players, displays player names and team points.
        """
        pass

    @abc.abstractmethod
    def dealerMsg(self, dealer):
        """Passes the Player that is the dealer.

        For human players, displays dealers name.
        """
        pass

    @abc.abstractmethod
    def topCardMsg(self, top_card):
        """Passes the Card turned up in the kitty.

        For human players, displays the top card.
        """
        pass

    @abc.abstractmethod
    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        """Passes results of a round (5 trick stint).

        For human players, displays takers, points won, and # of tricks taken.
        """
        pass

    @abc.abstractmethod
    def orderUpMsg(self, player, top_card):
        """Passes Player that ordered up and the top Card.

        For human players, displays orderers name and card ordered up
        """
        pass

    @abc.abstractmethod
    def deniedUpMsg(self, player):
        """Passes Player that denied ordering up.

        For human players, displays deniers name.
        """
        pass

    @abc.abstractmethod
    def orderedTrumpMsg(self, player, trump_suit):
        """Passes Player that ordered a trump suit.

        For human players, displays the orderers name and
        suit they ordered.
        """
        pass

    @abc.abstractmethod
    def deniedTrumpMsg(self, player):
        """Passes Player that denied ordering a trump suit.

        For human players, displays deniers name.
        """
        pass

    @abc.abstractmethod
    def gameResultsMsg(self):
        """TODO"""
        pass

    @abc.abstractmethod
    def misdealMsg(self):
        """Called when a misdeal occurs and that a new dealer is selected.

        For human players, displays that a misdeal occurred.
        """
        pass

    @abc.abstractmethod
    def leaderMsg(self, leader):
        """Passes Player that leads the trick.

        For human players, displays dealers name.
        """
        pass

    @abc.abstractmethod
    def playedMsg(self, player, card):
        """Passes Player and the card that they played.

        For human players, displays the name of the player and card played.
        """
        pass

    @abc.abstractmethod
    def takerMsg(self, taker):
        """Passes Player that took the trick.

        For human players, displays takers name.
        """
        pass

    @abc.abstractmethod
    def penaltyMsg(self, player, card):
        """Passes Player that reneged.

        For human players, displays reneger, card reneged, and points awarded.
        """
        pass

    @abc.abstractmethod
    def invalidSuitMsg(self):
        """Called when this Player misdeals.

        For human players, informs player to call a valid suit.
        """
        pass

    @abc.abstractmethod
    def trickStartMsg(self):
        """Called when a new trick starts.

        For human players, displays that a new trick has started / is used for
        console spacing.
        """
        pass

    @abc.abstractmethod
    def newTrumpMsg(self, trump_suit):
        """Called when there is a new trump.

        For human players, displays new trump.
        """
        pass

#    @abc.abstractmethod
#    def passMsg(self, msg):
#        """Recieves game information and processes it for the player.
#
#        Possible messages and their purposes:
#            {'type': 'points',
#             'teams': (Team, Team)}
#            Updated points after round, points can be accessed in the Team
#            object through team.points.
#
#            {'type': 'dealer',
#             'player': Player}
#            What player is the new dealer.
#
#            {'type': 'misdeal'}
#            Last round was a misdeal and a new round will start.
#
#            {'type': 'top_card',
#             'top_card': Card}
#            Top card turned up during the dealing phase.
#
#            {'type': 'ordered_up',
#             'player': Player}
#            Player that ordered the top card up.
#
#            {'type': 'denied_up',
#             'player': Player}
#            Player that denied ordering the top card up.
#
#            {'type': 'invalid_suit'}
#            This player tried to call an invalid suit for trump.
#
#            {'type': 'ordered_trump',
#             'player': Player}
#            Player that ordered trump.
#
#            {'type': 'denied_trump',
#             'player': Player}
#            Player that denied trump.
#
#            {'type': 'trick_start'}
#            New trick is starting.
#
#            {'type': 'card_played',
#             'player': Player,
#             'card': Card}
#            Card played by a player during a trick.
#
#            {'type': 'new_taker',
#             'taker': Player}
#            Taker of the previous trick.
#
#            {'type': 'round_results',
#             'taking_team': Team,
#             'points_scored': points,
#             'team_tricks': tricks}
#            Results of a round including points scored and number of tricks
#            taken by the team that won the round.
#
#            {'type': 'penalty',
#             'player': Player,
#             'card': Card}
#            Player that reneged and what card they played to renege
#        """
#        pass
