from euchre.players.player import Player
import abc


class BasicAIPlayer(Player, abc.ABC):
    """A Player class that returns valid responses."""
    def __init__(self, name='AI'):
        Player.__init__(self, name)

    def updateHand(self, cards):
        self.hand = cards

    def orderUp(self):
        return False

    def orderTrump(self):
        return False

    def callTrump(self, upSuit):
        return None

    def goAlone(self):
        return False

    def playCard(self, leader, cardsPlayed, trump):
        # Play an arbitrary card if player is leader
        if leader is self:
            card = self.hand.pop()
        else:
            # Play an arbitrary valid card
            leadSuit = cardsPlayed[leader][-1].suit
            playable = [card for card in self.hand if card.getSuit(
                        trump) == leadSuit]
            card = playable[0] if playable else self.hand[0]
            self.hand.remove(card)

        return card

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
