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
    def passMsg(self, msg, content=None):
        """Recieves messages that pass game information to the player.

        Valid values for msg:
            "points":
                content: (team1 points, team2 points)
            "misdeal"
                content: None
            "leader":
                content: Player
            "played":
                content: (player, card)
            "taker":
                content: Player
            "deniedUp":
                content: Player
            "allPassed":
                content: isTrump
            "deniedTrump":
                content: Player
            "penalty"
                content: (Player, points)
            "invalidSuit"
                content: None
        """
        pass
