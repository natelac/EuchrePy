class Team:
    """"Stores basic data for teams.

    Attributes:
        points: How many points the team has.
    """
    def __init__(self, player1, player2):
        self.points = 0
        self._p1 = player1
        self._p2 = player2
        self._p1.team = self
        self._p2.team = self

    def getPlayers(self):
        """Gets all players on the team.

        Returns:
            (list): Players on team.
        """
        return [self._p1, self._p2]

    def getTeammate(self, player):
        """Gets the teammates of the passed player.

        Returns:
            (Player): Teammate of passed player
        """
        if player is self._p1:
            return self._p2
        elif player is self._p2:
            return self._p1
        else:
            return None
