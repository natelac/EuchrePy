from _player import Player
import abc

class HumanPlayer(Player, abc.ABC):
    def __init__(self, name='Human'):
        Player.__init__(self, name)

    def orderUp(self, orderInfo):
        self._printCards()
        self._recoverTrick(orderInfo, True)
        ans = input('Order up? y/n\n')
        return ans == 'y'

    def orderTrump(self, orderInfo):
        self._recoverTrick(orderInfo, False)
        ans = input('Call trump? y/n\n')
        if ans == 'y':
            return True
        else:
            return False

    def _printCards(self):
        print('Cards: ', end="")
        print(*self.hand,sep=", ")

    def _recoverTrick(self, orderInfo, firstPass):
        if firstPass:
            print("The top card is", orderInfo['topCard'])
        players = orderInfo['players']
        for player in orderInfo['players']:
            if player is self:
                break
            else:
                print(f"{player} passed ordering {'up' if firstPass else 'trump'}")

    def orderUpResults(self, players, deniedOrderUp):
        seen = False
        for player in players:
            if player is self:
                seen = True
            elif seen == True:
                print(f"""{player} {'did' if deniedOrderUp[player] else "didn't"} pass ordering up""")


    def orderTrumpResults(self, players, deniedOrderTrump):
        seen = False
        for player in players:
            if player is self:
                seen = True
            elif seen == True:
                print(f"""{player} {'did' if deniedOrderTrump[player] else "didn't"} pass ordering trump""")

    def goAlone(self):
        ans = input('Go alone? y/n\n')
        return ans == 'y'

    def playTrick(self, orderInfo, playedCards, downCards):
        cards = [str(card) for card in self.hand]
        print('Your cards:', cards)
        ans = input('Enter card to play\n')
        while ans not in cards:
            ans = input('Not a card in your hand.\n')
        cardIndex = cards.index(ans)
        card = self.hand.pop(cardIndex)
        self._playedCards.append(card)
        return card

    def playCard(self, cardsPlayed, game):
        cards = [str(card) for card in self.hand]
        # print(cardsPlayed)
        print("Top Card:", game.topCard)
        print("Trump Suit:", game.trump)
        print('Your cards:', cards)
        ans = input('Enter card to play\n')
        while ans not in cards:
            ans = input('Not a card in your hand.\n')
        cardIndex = cards.index(ans)
        card = self.hand.pop(cardIndex)
        self._playedCards.append(card)
        return card

    def recieveError(self,error):
        print(error)

    def recieveUpdate(self, update):
        print(update)

    def callTrump(self, orderInfo):
        ans = input('What suit? (C,S,H,D) \n')
        return ans
