class Team:
    def __init__(self, player1, player2):
        self._points = 0
        self._p1 = player1
        self._p2 = player2
        self._p1.team = self
        self._p2.team = self

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    # def _updatePoints(self):
    #     self._points = self._p1.points + self._p2.points

    # def getOpponentTeam(self):
    #     for team in Team.teams:
    #         if player not in team.getPlayers():
    #             return team
    #     return None

    def getPlayers(self):
        return [self._p1, self._p2]

    def getTeammate(self, player):
        if player is self._p1:
            return self._p2
        elif player is self._p2:
            return self._p1
        else:
            return None

    def msgPlayers(self, msg):
        _p1.passMsg(msg)
        _p2.passMsg(msg)
        return
