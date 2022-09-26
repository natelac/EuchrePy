import abc

from euchre.players.player import Player



class BasicAIPlayer(Player, abc.ABC):
    """A Player class that returns valid responses.
    """

    def __init__(self, name='AI'):
        Player.__init__(self, name)

    # Decision methods that require a return value
    # -------------------------------------------------------------------------
    def orderUp(self):
        return False

    def discardCard(self, top_card):
        # Put an arbitrary card in kitty
        discard_card = self.hand.pop()
        self.hand.append(top_card)
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
            playable = [card for card in self.hand if card.getSuit(trump) == leadSuit]
            card = playable[0] if playable else self.hand[0]
            self.hand.remove(card)

        return card

    # Information updates that don't require a return value
    # -------------------------------------------------------------------------
    def updateHand(self, cards):
        self.hand = cards

    def pointsMsg(self, team1, team2):
        pass

    def dealerMsg(self, dealer):
        pass

    def topCardMsg(self, top_card):
        pass

    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        pass

    def orderUpMsg(self, player, top_card):
        pass

    def deniedUpMsg(self, player):
        pass

    def orderedTrumpMsg(self, player, trump_suit):
        pass

    def deniedTrumpMsg(self, player):
        pass

    def gameResultsMsg(self, winning_team):
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
