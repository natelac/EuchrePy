import numpy as np
from deck import Deck
# from card import Card
# from team import Team
# from player import Player
# from consolehuman import HumanPlayer
# from basicai import BasicAIPlayer


class StandardGame:
    """Standard game of euchre
    Source: https://en.wikipedia.org/wiki/Euchre
    """

    def __init__(self, team1, team2):
        # Game info
        self.deck = Deck()
        self.players = []
        self.team1 = team1
        self.team2 = team2
        self.oppoTeam = {team1: team2, team2: team1}
        self.seatPlayers()

        # Trick Info
        self.topCard = None
        self.trump = None
        self.maker = None

    def play(self):
        """Plays a game of euchre until a team reaches 10 points."""
        if len(self.players) != 4:
            raise AssertionError(f"Euchre requires 4 players to play")

        # Game Loop
        while not self.getWinner():
            self.msgPlayers({'type': 'points',
                             'teams': (self.team1, self.team2)})
            makerSelected = self.dealPhase()
            if makerSelected:
                self.playTricks()
            else:
                self.msgPlayers({'type':'misdeal'})
            self.newDealer()

    def playTricks(self):
        """Plays the 5 tricks."""
        # Initialize trick information
        goingAlone = self.maker.goAlone()
        cardsPlayed = {} # Maps player to cards played
        tricksTaken = {} # Maps players to tricks taken
        if goingAlone:
            # Skip team-mate of player going alone
            for player in self.players:
                if self.maker.getTeammate() is not player:
                    cardsPlayed[player] = []
                    tricksTaken[player] = 0
        else:
            cardsPlayed = {player: [] for player in self.players}
            tricksTaken = {player: 0 for player in self.players}

        taker = self.players[1] # Init taker to player left of dealer
        leaderList = [] # List of players that lead for all 5 tricks
        self.msgPlayers({'type': 'new_leader', 'leader': player})

        # Play tricks
        for j in range(5):
            leaderList.append(taker) # Taker of previous round leads

            # Play a trick
            for i in range(4):
                idx = (self.players.index(taker) + i) % 4
                player = self.players[idx]
                if goingAlone and self.maker.getTeammate() is player:
                    # Skip teammate of player going alone
                    continue
                card = player.playCard(taker, cardsPlayed, self.trump)
                cardsPlayed[player].append(card)
                self.msgPlayers({'type': 'card_played',
                                 'player': player,
                                 'card': card},
                                exclude=player)

            # Decide Taker
            trick = {player: cards[j] for player, cards in cardsPlayed.items()}
            ledSuit = trick[taker].suit
            taker = max(trick,
                        key=lambda player: trick[player].value(
                            ledSuit, self.trump))
            self.msgPlayers({'type': 'new_taker', 'taker': taker})
            tricksTaken[taker] += 1

        # Reneging
        renegers = self.checkForReneges(leaderList, cardsPlayed, goingAlone)
        if renegers:
            self.penalize(renegers)

        # Otherwise score round
        else:
            self.scoreRound(tricksTaken, goingAlone)

    def scoreRound(self, tricksTaken, goingAlone):
        """Messages players winner and points won."""
        # Count tricks taken per team
        teamTricks = {self.team1: 0, self.team2: 0}
        for player, taken in tricksTaken.items():
            teamTricks[player.team] += taken
        takingTeam = max(teamTricks, key=teamTricks.get)

        # Figure out points
        points = 1
        if self.maker in takingTeam.getPlayers():
            if goingAlone and teamTricks[takingTeam] == 5:
                points = 4
            elif teamTricks[takingTeam] == 5:
                points = 2
        else:
            points = 2

        # Finalize results
        takingTeam.points += points
        self.msgPlayers({
                         'type': 'roundResults',
                         'taking_team': takingTeam,
                         'points': points,
                         'team_tricks': teamTricks[takingTeam]
                        })

    def msgPlayers(self, msg exclude=None):
        """Messages all players with a type of message and it's content.

        See Player.passMsg() for valid values for msg.

        Args:
            msg: A string identifying type of message.
            content: Content of message to be sent.
            exclude: Players that should NOT recieve the message.
        """
        for player in self.players:
            if player is not exclude:
                player.passMsg(msg)

    def penalize(self, renegers):
        """Penalizes the renegers by giving 2 points to the opposing team.

        Args:
            renegers: A list of players to be penalized
        """
        for player in renegers:
            team = self.oppoTeam[player.team]
            team.points += 2

    def checkForReneges(self, leaderList, cardsPlayed, goingAlone):
        """Figures out who reneged.

        Args:
            leaderList: A list of players ordered by when they lead the trick.
            cardsPlayed: A dict mapping players to a list of cards played.
                The list of cards is ordered by trick.

        Returns:
            A list of players that reneged and need to be penalized.
        """
        renegers = []

        # Check each trick
        for j in range(5):
            leader = leaderList[j]
            leadSuit = cardsPlayed[leader][j].getSuit(self.trump)

            # Add player to renengers if invalid card played
            for player in self.players:
                if goingAlone and self.maker.getTeammate() is player:
                    continue
                cards = cardsPlayed[player][j:]
                playable = [card for card in cards if card.getSuit(
                    self.trump) == leadSuit]
                if (len(playable) != 0) and (cards[0] not in playable):
                    valid = False
                else:
                    valid = True
                if not valid:
                    self.msgPlayers({'type': 'penalty',
                                     'player': player,
                                     'card': cards[0]})
                    renegers.append(player) if player not in renegers else renegers
        return renegers

    def resetTrick(self):
        """Resets the information used in each trick."""
        self.topCard = None
        self.trump = None
        self.maker = None

    def seatPlayers(self):
        """Seats the players randomly around table (preserving teams).
        """
        self.players = []
        t1 = self.team1.getPlayers()
        t2 = self.team2.getPlayers()

        # Shuffle within each team
        np.random.shuffle(t1)
        np.random.shuffle(t2)

        # Shuffle order of teams
        teams = [t1, t2]
        np.random.shuffle(teams)

        # Team mates must be across from each other
        self.players.append(teams[0][0])
        self.players.append(teams[1][0])
        self.players.append(teams[0][1])
        self.players.append(teams[1][1])

    def dealPhase(self):
        """Deals cards and determines trump.

        Returns:
            True if there was a misdeal, False otherwise.
        """
        # Distribute Cards
        self.deck.shuffle()
        hands = self.deck.deal()
        for i in range(4):
            self.players[i].hand = hands[i]
        self.kitty = hands[4]
        self.topCard = self.kitty[0]

        # Order Up and Trump phases
        allPassed = self.orderPhase()
        if allPassed:
            allPassed = self.trumpPhase()

        return not allPassed

    def orderPhase(self):
        """Asks all players if they want to order up the top card.

        Returns:
            True if everyone passes ordering up, otherwise False.
        """
        # Ask players if they want to order up top card
        for player in self.players:
            orderUp = player.orderUp()
            if orderUp:
                self.maker = player
                self.trump = self.topCard.suit
                return False
            else:
                self.msgPlayers({'type': 'denied_up', 'player': player},
                                exclude=player)
        return True

    def trumpPhase(self):
        """Asks all players if they want to order trump.

        Returns:
            True if everyone passes ordering trump, otherwise False
        """
        # Ask players if they want to order trump
        for player in self.players:
            orderTrump = player.orderTrump()
            if orderTrump:
                call = player.callTrump()

                # Require valid trump that isn't top card suit
                while not self.validTrump(call):
                    player.passMsg({'type':'invalid_suit'})
                    call = player.callTrump()

                self.maker = player
                self.trump = call
                return False
            else:
                self.msgPlayers({'type': 'denied_trump', 'player': player},
                                exclude=player)

        return True

    def validTrump(self, suit):
        """Checks if a trump call is valid.

        Args:
            The suit that a player has called.

        Returns:
            True if the trump is valid, otherwise False.
        """
        if not suit in ['C', 'S', 'H', 'D']:
            return False
        return suit != self.topCard.suit

    def newDealer(self):
        """Selects the new dealer.

        Rotates the player order so the player to the left of the dealer is the new dealer.
        """
        newDealer = self.players.pop(0)
        self.players.append(newDealer)

    def getWinner(self):
        """Fetches the winner.

        Returns:
            Player that won, or if there is no winner, None.
        """
        return None
