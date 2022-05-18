import abc

class Player(abc.ABC):
    """Base Player class

    Attributes:
        name: Name of the player
        team: Team that the player is on
        hand: List of cards in the players hand
    """

    def __init__(self, name=''):
        self.name = name
        self.team = None
        self.hand = None
        self._playedCards = []

    def __str__(self):
        """Gets name of player"""
        return self.name

    def getTeammate(self):
        """Gets teammate

        Returns:
            Player that is on the same team as this Player."""
        return self.team.getTeammate(self)

    @abc.abstractmethod
    def updateHand(self, cards):
        """Updates cards in players hand
        """
        pass

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
    def passMsg(self, msg):
        """Recieves game information and processes it for the player.

        Possible messages and their purposes:
            {'type': 'points',
             'teams': (Team, Team)}
            Updated points after round, points can be accessed in the Team
            object through team.points.

            {'type': 'dealer',
             'player': Player}
            What player is the new dealer.

            {'type': 'misdeal'}
            Last round was a misdeal and a new round will start.

            {'type': 'top_card',
             'top_card': Card}
            Top card turned up during the dealing phase.

            {'type': 'ordered_up',
             'player': Player}
            Player that ordered the top card up.

            {'type': 'denied_up',
             'player': Player}
            Player that denied ordering the top card up.

            {'type': 'invalid_suit'}
            This player tried to call an invalid suit for trump.

            {'type': 'ordered_trump',
             'player': Player}
            Player that ordered trump.

            {'type': 'denied_trump',
             'player': Player}
            Player that denied trump.

            {'type': 'trick_start'}
            New trick is starting.

            {'type': 'card_played',
             'player': Player,
             'card': Card}
            Card played by a player during a trick.

            {'type': 'new_taker',
             'taker': Player}
            Taker of the previous trick.

            {'type': 'round_results',
             'taking_team': Team,
             'points_scored': points,
             'team_tricks': tricks}
            Results of a round including points scored and number of tricks
            taken by the team that won the round.

            {'type': 'penalty',
             'player': Player,
             'card': Card}
            Player that reneged and what card they played to renege
        """
        pass
