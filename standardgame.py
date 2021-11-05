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
            raise AssertionError(
                f"Euchre requires 4 players to play")

        # Game Loop
        while not self.getWinner():
            self.msgPlayers("points", (self.team1, self.team2))
            makerSelected = self.dealPhase()
            if makerSelected:
                self.playTricks()
            else:
                self.msgPlayers("misdeal")
            self.newDealer()

    def playTricks(self):
        """Plays the 5 tricks."""
        # Initialize Lists/Dicts
        goingAlone = self.maker.goAlone()
        cardsPlayed = {player: [] for player in self.players}
        tricksTaken = {player: 0 for player in self.players}

        # Start Deal
        taker = self.players[1]
        leaderList = []
        self.msgPlayers("leader", taker)

        # Play Tricks
        for j in range(5):
            leaderList.append(taker)

            # A trick
            for i in range(4):
                idx = (self.players.index(taker) + i) % 4
                player = self.players[idx]
                card = player.playCard(taker, cardsPlayed, self.trump)
                cardsPlayed[player].append(card)
                self.msgPlayers("played", (player, card), exclude=player)

            # Decide Taker
            trick = {player: cards[j] for player, cards in cardsPlayed.items()}
            ledSuit = trick[taker].suit
            taker = max(trick,
                        key=lambda player: trick[player].value(
                            ledSuit, self.trump))
            self.msgPlayers("taker", taker)
            tricksTaken[taker] += 1

        # Reneging
        renegers = self.checkForReneges(leaderList, cardsPlayed, )
        if renegers:
            self.penalize(renegers)
        return

    def msgPlayers(self,
                   msg: str,
                   content: str = None,
                   exclude: list = None):
        """Messages all players with a type of message and it's contentself.

        See Player.passMsg() for valid strings for msg.

        Args:
            msg: Message type to send.
            content: Content of message to be send.
            exclude: Players that should NOT recieve the message.
        """
        for player in self.players:
            if player is not exclude:
                player.passMsg(msg, content)

    def penalize(self, renegers):
        """Penalizes the renegers by giving 4 points to the opposing team."""
        for player in renegers:
            team = self.oppoTeam[player.team]
            team.points += 4

    def checkForReneges(self, leaderList, cardsPlayed):
        """Returns a list of players that reneged during the last round."""
        renegers = []

        # Check Tricks
        for j in range(5):
            leader = leaderList[j]
            leadSuit = cardsPlayed[leader][j].getSuit(self.trump)

            # Check Player's Card
            for player in self.players:
                cards = cardsPlayed[player][j:]
                playable = [card for card in cards if card.getSuit(
                    self.trump) == leadSuit]
                if (len(playable) != 0) and (cards[0] not in playable):
                    valid = False
                else:
                    valid = True
                if not valid:
                    self.msgPlayers("penalty", (player, cards[0]))
                    renegers.append(
                        player) if player not in renegers else renegers
        return renegers

    def resetTrick(self):
        """Resets the information used in each trick"""
        self.topCard = None
        self.trump = None
        self.maker = None

    def seatPlayers(self):
        """Seats the players randomly around table (preserving teams)
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
        """Enters the dealing phase, returns False if no maker selected

        Modifies
        ---------------------
        self.deck
        self.players
        self.kitty
        self.topCard
        self.allPassed
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
        """Handles the order up phase, returns True if everyone
        passes ordering up
        """
        # Ask players if they want to order up top card
        for player in self.players:
            orderInfo = self.orderInfo(player)
            orderUp = player.orderUp(orderInfo)
            if orderUp:
                self.maker = player
                self.trump = self.topCard.suit
                return False
            else:
                self.msgPlayers("deniedUp", player, exclude=player)
        return True

    def trumpPhase(self):
        """Handles the order trump phase, returns true

        Modifies
        -----------------------
        self.trump
        self.maker
        self.deniedTrump
        """
        # Ask players if they want to order trump
        for player in self.players:
            orderInfo = self.orderInfo(player)
            orderTrump = player.orderTrump(orderInfo)
            if orderTrump:
                call = player.callTrump(orderInfo)

                # Require valid trump that isn't top card suit
                while not self.validTrump(call):
                    player.passMsg("invalidSuit")
                    call = player.callTrump(orderInfo)

                self.maker = player
                self.trump = call
                return False
            else:
                self.msgPlayers("deniedTrump", player, exclude=player)

        return True

    def validTrump(self, suit):
        """Returns True if a card is a valid trump call
        """
        if not suit in ['C', 'S', 'H', 'D']:
            return False
        return suit != self.topCard.suit

    def newDealer(self):
        """Rotates the player order so the player to the left of the dealer is the dealer
        """
        newDealer = self.players.pop(0)
        self.players.append(newDealer)

    def orderInfo(self, player):
        """Dictionary of info about the trick for player to make a decision with

        Contains enough information for the Player class to understand the
        current state of the trick during the dealing phase

        Returns
        ----------
        dict
            team1: Team
                The first team (arbitrary)
            team2: Team
                The second team (arbitrary)
            players: list(Player)
                All 4 players, in order of turn (idx=3 is dealer)
            topCard: Card
                The card that was turned over
        """
        orderInfo = {
            'team1': self.team1,
            'team2': self.team2,
            'players': self.players,
            'topCard': self.topCard
        }
        return orderInfo

    def getWinner(self):
        """Returns the winning player or None
        """
        return None
