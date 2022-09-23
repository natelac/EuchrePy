import abc

from euchre.players.player import Player



class SmartAIPlayer(Player, abc.ABC):
    """A Player class that returns smart responses.

    TODO:
    Here are some things that make this smarter than the basic AI:
    - Orders up jack if it's the dealer
    - Orders up if it has at least 3 trump cards
        and the top card goes to its team
    - Orders trump if it has 3 or more cards of the same suit
    - Plays highest card if it wins the trick
    - Plays lowest card if highest card can't win
    - Plays random trump if can't follow lead
    """

    def __init__(self, name='AI'):
        Player.__init__(self, name)

    def getLowestCard(self, led_card, trump_suit):
        # Return lowest value card
        pass

    def getHighestCard(self, led_card, trump_suit):
        # Return high value card
        pass

    def updateHand(self, cards):
        self.hand = cards

    def orderUp(self):
        return False

    # Decision methods that require a return value
    # -------------------------------------------------------------------------

    def discardCard(self, top_card):
        # Put lowest valued card in the kitty
        self.hand.append(top_card)
        values = {}
        for card in self.hand:
            values[card] = card.value(card.suit, top_card.suit)
        discard_card = max(values, key=values.get)
        self.hand.remove(discard_card)
        return discard_card

    def orderTrump(self):
        return False

    def callTrump(self, up_suit):
        return None

    def goAlone(self):
        return False

    def playCard(self, leader, cards_played, trump):
        # Play an arbitrary card if player is leader
        if leader is self:
            card = self.hand.pop()
        else:
            # Play an arbitrary valid card
            leadSuit = cards_played[leader][-1].suit
            playable = [card for card in self.hand if card.getSuit(
                        trump) == leadSuit]
            card = playable[0] if playable else self.hand[0]
            self.hand.remove(card)

        return card

    # Information updates that don't require a return value
    # -------------------------------------------------------------------------

    def pointsMsg(self, team1, team2):
        pass

    def dealerMsg(self, dealer):
        pass

    def topCardMsg(self, top_card):
        pass

    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        pass

    def orderedUpMsg(self, player, top_card):
        pass

    def deniedUpMsg(self, player):
        pass

    def orderedTrumpMsg(self, player, trump_suit):
        pass

    def deniedTrumpMsg(self, player):
        pass

    def gameResultsMsg(self):
        pass

    def misdealMsg(self):
        pass

    def leaderMsg(self, leader):
        pass

    def playedMsg(self, player, card):
        pass

    def takerMsg(self, taker):
        pass

    def penaltyMsg(self, player, card):
        pass

    def invalidSuitMsg(self):
        pass

    def trickStartMsg(self):
        pass

    def newTrumpMsg(self, trump):
        pass
