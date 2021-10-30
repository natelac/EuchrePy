from player import Player
import abc

class BasicAIPlayer(Player, abc.ABC):
    def __init__(self, name='AI'):
        Player.__init__(self, name)

    def orderUp(self, orderInfo):
        # print(self.name, "didn't order up")
        return False

    def orderTrump(self, orderInfo):
        return False
        # if self == orderInfo['players'][3]

    def callTrump(self, orderInfo):
        return None

    def goAlone(self):
        # print(self.name, "didn't go alone")
        return False

    def orderUpResults(self, players, deniedOrderUp):
        return

    def orderTrumpResults(self, players, deniedOrderTrump):
        return

    def playCard(self, leader, cardsPlayed, trump):
        if leader is self:
            card = self.hand.pop()
        else:
            leadSuit = cardsPlayed[leader][-1].suit
            playable = [card for card in self.hand if card.getSuit(trump) == leadSuit]
            if playable:
                card = playable[0]
            else:
                card = self.hand.pop()
        print(self.name, "played", card)
        return card

    def passError(self, error):
        print("Error for",self.name,":",error)

    def passMsg(self, msg):
        pass
