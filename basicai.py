from player import Player
import abc


class BasicAIPlayer(Player, abc.ABC):
    """A Player class that returns valid responses."""
    def __init__(self, name='AI'):
        Player.__init__(self, name)

    def orderUp(self):
        return False

    def orderTrump(self):
        return False

    def callTrump(self):
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

    def passMsg(self, msg, content):
        pass
