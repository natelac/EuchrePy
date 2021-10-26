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
        self._points = 0

        self.team = None
        self.hand = None
        self._playedCards= []


    def __str__(self):
        return self.name

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points
        # if self.team:
        #     self.team._updatePoints()

    def getTeamPoints(self):
        return self.team.points

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
    def goAlone(self):
        pass

    @abc.abstractmethod
    def playTrick(self):
        pass

    @abc.abstractmethod
    def recieveError(self, error):
        pass

    # @abc.abstractmethod
    # def inform(self,msg):
    """Inform the player object that something has happened, like that everyone
    passed ordering trump
    """
    #     pass
