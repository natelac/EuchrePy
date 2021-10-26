from _player import Player
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

    def goAlone(self):
        # print(self.name, "didn't go alone")
        return False

    def orderUpResults(self, players, deniedOrderUp):
        return

    def orderTrumpResults(self, players, deniedOrderTrump):
        return

    def playTrick(self,orderInfo, playedCards, downCards):
        card = self.hand.pop(0)
        self._playedCards.append(card)
        return card

    def playCard(self, cardsPlayed, game):
        card = self.hand.pop()
        print(self.name, "played", card)
        return card

    def recieveError(self, error):
        print("Error for",self.name,":",error)

    def recieveUpdate(self, update):
        print(update)

    def callTrump(self, orderInfo):
        pass
