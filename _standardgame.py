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
        self.seatPlayers()

        # Set's trick info
        self.topCard = None
        self.deniedOrderUp = {  self.players[0]: False,
                                self.players[1]: False,
                                self.players[2]: False,
                                self.players[3]: False}
        self.deniedOrderTrump = {   self.players[0]: False,
                                    self.players[1]: False,
                                    self.players[2]: False,
                                    self.players[3]: False}
        self.trump = None
        self.maker = None

    def play(self):
        """Starts the game
        """
        if len(self.players) != 4:
            raise AssertionError("Euchre requires 4 players to play")
        while (not self.getWinner()):
            makerSelected = self.dealPhase()
            if makerSelected:
                self.playTrick()
            else:
                self.newDealer()
                continue

    def playTrick(self):
        goingAlone = self.maker.goAlone()
        if goingAlone:
            print("For now ignoring go alone")
        cardsPlayed = {
            self.players[0]: [],
            self.players[1]: [],
            self.players[2]: [],
            self.players[3]: []
        }
        tricksTaken = {
            self.players[0]: 0,
            self.players[1]: 0,
            self.players[2]: 0,
            self.players[3]: 0
        }
        taker = self.players[1]
        for j in range(5):
            for i in range(4):
                idx = ( self._getPlayerIdx(taker) + i ) % 4
                player = self.players[idx]
                card = player.playCard(cardsPlayed, self)
                cardsPlayed[player].append(card)
            trick = {player:cards[j] for player,cards in cardsPlayed.items()}
            taker = self._evalCards(trick, taker)
            print("The taker is:", taker)
            tricksTaken[taker] += 1
        # Return team with most tricks taken
        return

    def _validCard(self, card, trick, taker):
        '''Checks if a card is valid
        '''

    def _evalCards(self, trick, taker):
        ledSuit = trick[taker].suit
        return max(trick, key=lambda player: trick[player].value(ledSuit, self.trump))

    def forAll(self, func):
        for player in self.players:
            eval('player.' + func)


    def resetTrick(self):
        self.topCard = None
        self.deniedOrderUp = {  self.players[0]: False,
                                self.players[1]: False,
                                self.players[2]: False,
                                self.players[3]: False}
        self.deniedOrderTrump = {   self.players[0]: False,
                                    self.players[1]: False,
                                    self.players[2]: False,
                                    self.players[3]: False}
        self.trump = None
        self.maker = None

    def seatPlayers(self):
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
        # Distributing cards
        self.deck.shuffle()
        hands = self.deck.deal()
        for i in range(4):
            self.players[i].hand = hands[i]
        self.kitty = hands[4]
        self.topCard = self.kitty[0]

        # Ordering up or selecting trump
        allPassed = self.orderPhase()
        self.forAll("orderUpResults(self.players, self.deniedOrderUp)")
        if allPassed:
            allPassed = self.trumpPhase()
            self.forAll("orderTrumpResults(self.players, self.deniedOrderTrump)")
        return not allPassed

    def orderPhase(self):
        """Handles the order up phase, returns True if everyone
        passes ordering up

        Modifies
        --------------------
        self.topCard
        self.maker
        self.deniedOrderUp
        """
        for player in self.players:
            orderInfo = self.orderInfo(player)
            orderUp = player.orderUp(orderInfo)
            if orderUp:
                self.maker = player
                self.trump = self.topCard.suit
                return False
            else:
                self.deniedOrderUp[player] = True
        return True

    def trumpPhase(self):
        """Handles the order trump phase, returns true

        Modifies
        -----------------------
        self.trump
        self.maker
        self.deniedOrderTrump
        """
        for player in self.players:
            orderInfo = self.orderInfo(player)
            orderTrump = player.orderTrump(orderInfo)
            if orderTrump:
                call = player.callTrump(orderInfo)
                while not self.validTrump(call):
                    player.recieveError("Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")
                    call = player.callTrump(orderInfo)
                self.maker = player
                self.trump = call
                return False
            else:
                self.deniedOrderTrump[player] = True
        return True

    def validTrump(self, suit):
        """Returns True if a card is a valid trump call
        """
        if not suit in ['C','S','H','D']:
            return False
        return suit != self.topCard.suit

    def newDealer(self):
        """Rotates the player order so the player to the left of the dealer is the dealer
        """
        newDealer = self.players.pop(0)
        self.players.append(newDealer)

    def orderInfo(self,player):
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

    def getDealer(self):
        return self.players[3]

    def getDealer(self, player):
        dealer = self.players[3]
        if dealer is player:
            return 'self'
        elif dealer is player.getTeammate():
            return 'partner'
        else:
            return 'opponent'

    def getRotationNum(self, player):
        loc = ['first','second','third','dealer']
        locIdx = self.players.index(player)
        return loc[locIdx]


    def isDealer(self, player):
        return self.players[3] is player

    def getWinner(self):
        """Returns the winning player or None
        """
        return None

    def _getPlayerIdx(self, player):
        for i, playeri in enumerate(self.players):
            if player is playeri:
                return i
        raise AssertionError("Player is not in game")


    def leftPlayer(self, player):
        """Returns the player to the left
        """
        left_idx = (self.players.index(player) + 1) % 4
        return self.players[left_idx]
