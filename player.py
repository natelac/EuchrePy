import abc


class Player(abc.ABC):
    """Base Player class

    Attributes
    ----------
    name : str
        Name of the player
    team : Team
        Team that the player is on
    hand : list(Card)
        List of cards in the players hand

    """

    def __init__(self, name=''):
        self.name = name
        self.team = None
        self.hand = None
        self._playedCards = []

    def __str__(self):
        return self.name

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    def getTeammate(self):
        return self.team.getTeammate(self)

    @abc.abstractmethod
    def orderUp(self, orderUpInfo):
        pass

    @abc.abstractmethod
    def orderTrump(self, orderInfo):
        pass

    @abc.abstractmethod
    def callTrump(self, orderInfo):
        pass

    @abc.abstractmethod
    def playCard(self, leader, cardsPlayed, trump):
        pass

    @abc.abstractmethod
    def goAlone(self):
        pass

    @abc.abstractmethod
    def passMsg(self, msg, content=None):
        """
        msg:
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
