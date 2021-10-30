from _deck import Deck
from _card import Card
from _team import Team
# from consolehuman import HumanPlayer
# from basicai import BasicAIPlayer
import numpy as np

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
        self._seatPlayers()

        # Trick Info
        self.topCard = None
        self.trump = None
        self.maker = None
        self.deniedOrderUp = {player: False for player in self.players}
        self.deniedOrderTrump = {player: False for player in self.players}

    def play(self):
        """Starts the game
        """
        if len(self.players) != 4:
            raise AssertionError("Euchre requires 4 players to play")
        while (not self._getWinner()):
            self._msgPlayers(f"Team1 has {self.team1.points} points\tTeam2 has {self.team2.points} points")
            makerSelected = self._dealPhase()
            if makerSelected:
                self._playTricks()
            else:
                self._newDealer()
                continue

    def _playTricks(self):
        goingAlone = self.maker.goAlone()
        cardsPlayed = {player: [] for player in self.players}
        tricksTaken = {player: 0 for player in self.players}

        # Player to left of dealer starts
        taker = self.players[1]
        leaderList = []
        self._msgPlayers(f"{taker} starts the first trick")
        # There are 5 tricks
        for j in range(5):
            # Each player plays
            leaderList.append(taker)
            for i in range(4):
                idx = ( self.players.index(taker) + i ) % 4
                player = self.players[idx]
                card = player.playCard(taker, cardsPlayed, self.trump)
                cardsPlayed[player].append(card)
            trick = {player:cards[j] for player,cards in cardsPlayed.items()}
            ledSuit = trick[taker].suit
            taker = max(trick, key=lambda player: trick[player].value(ledSuit, self.trump))
            self._msgPlayers(f"{taker} takes the hand")
            tricksTaken[taker] += 1

        # Check for reneging
        renegers = self._checkForReneges(leaderList, cardsPlayed, )

        if renegers:
            self._penalize(renegers)
        return

    def _msgPlayers(self, msg, exclude=None):
        for player in self.players:
            if player is not exclude:
                player.passMsg(msg)

    def _penalize(self, renegers):
        for player in renegers:
            team = self.oppoTeam[player.team]
            team.points += 4

    def _checkForReneges(self, leaderList, cardsPlayed):
        renegers = []
        # Check each trick
        for j in range(5):
            leader = leaderList[j]
            leadSuit = cardsPlayed[leader][j].getSuit(self.trump)
            for player in self.players:
                cards = cardsPlayed[player][j:]
                playable = [card for card in cards if card.getSuit(self.trump) == leadSuit]
                if (len(playable) != 0) and (cards[0] not in playable):
                    valid = False
                else:
                    valid = True
                if not valid:
                    # Inform all players who messed up
                    print(player, "played an invalid card:",cards[0])
                    renegers.append(player) if player not in renegers else renegers
        return renegers

    def _resetTrick(self):
        self.topCard = None
        self.trump = None
        self.maker = None
        self.deniedOrderUp = {player: False for player in self.players}
        self.deniedOrderTrump = {player: False for player in self.players}

    def _seatPlayers(self):
        """Seats the players randomly around table (preserving teams)
        """
        self.players = []
        t1 = self.team1.getPlayers()
        t2 = self.team2.getPlayers()
        np.random.shuffle(t1)
        np.random.shuffle(t2)
        teams = [t1, t2]
        np.random.shuffle(teams)
        self.players.append(teams[0][0])
        self.players.append(teams[1][0])
        self.players.append(teams[0][1])
        self.players.append(teams[1][1])

    def _dealPhase(self):
        """Enters the dealing phase, returns False if no maker selected

        Modifies
        ---------------------
        self.deck
        self.players
        self.kitty
        self.topCard
        self.allPassed
        """
        # Distributing cards
        self.deck.shuffle()
        hands = self.deck.deal()
        for i in range(4):
            self.players[i].hand = hands[i]
        self.kitty = hands[4]
        self.topCard = self.kitty[0]

        # Ordering up or selecting trump
        allPassed = self._orderPhase()
        if allPassed:
            allPassed = self._trumpPhase()
        return not allPassed

    def _orderPhase(self):
        """Handles the order up phase, returns True if everyone
        passes ordering up

        Modifies
        --------------------
        self.topCard
        self.maker
        self.deniedOrderUp
        """
        for player in self.players:
            orderInfo = self._orderInfo(player)
            orderUp = player.orderUp(orderInfo)
            if orderUp:
                self.maker = player
                self.trump = self.topCard.suit
                return False
            else:
                self.deniedOrderUp[player] = True
                self._msgPlayers(f"{player} denied ordering up.", exclude=player )
        return True

    def _trumpPhase(self):
        """Handles the order trump phase, returns true

        Modifies
        -----------------------
        self.trump
        self.maker
        self.deniedOrderTrump
        """
        for player in self.players:
            orderInfo = self._orderInfo(player)
            orderTrump = player.orderTrump(orderInfo)
            if orderTrump:
                call = player.callTrump(orderInfo)
                while not self._validTrump(call):
                    player.recieveError("Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")
                    call = player.callTrump(orderInfo)
                self.maker = player
                self.trump = call
                return False
            else:
                self.deniedOrderTrump[player] = True
                self._msgPlayers(f"{player} denied ordering up.", exclude=player )
        return True

    def _validTrump(self, suit):
        """Returns True if a card is a valid trump call
        """
        if not suit in ['C','S','H','D']:
            return False
        return suit != self.topCard.suit

    def _newDealer(self):
        """Rotates the player order so the player to the left of the dealer is the dealer
        """
        newDealer = self.players.pop(0)
        self.players.append(newDealer)

    def _orderInfo(self,player):
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
        orderInfo ={
            'team1': self.team1,
            'team2': self.team2,
            'players': self.players,
            'topCard' : self.topCard
        }
        return orderInfo

    def _getWinner(self):
        """Returns the winning player or None
        """
        return None
