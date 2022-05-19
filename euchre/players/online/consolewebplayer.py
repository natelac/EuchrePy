from euchre.players import WebPlayer
import abc

class ConsoleWebPlayer(WebPlayer, abc.ABC):
    """A Player class that prints to and takes input from the console."""

    def __init__(self, updates, host='localhost', port=6001, name='WebPlayer'):
        WebPlayer.__init__(self, updates, host='localhost',
                           port=6001, name='WebPlayer')

    def updateHand(self, cards):
        self.hand = cards
        msg = {'message_type': 'update_hand',
               'new_hand': cards}
        self.sendMessage(msg)

    def orderUp(self):
        ans = self.request('order_up')
        return ans == 'y'

    def orderTrump(self):
        ans = self.request('order_trump')
        return ans == 'y'

    def callTrump(self, topSuit):
        ans = self.request('call_trump')
        while ans not in ['C', 'S', 'H', 'D'] and ans != topSuit:
            #TODO: Update player they played an invalid suit
            ans = self.request('call_trump')
        return ans

    def goAlone(self):
        ans = self.request('go_alone')
        return ans == 'y'

    def playCard(self, leader, cardsPlayed, trump):
        # Get card to play from user
        ans = self.request('play_card')
        while ans not in cards:
            #TODO: Update player that they played a card not in their hand
            ans = self.request('play_card')

        # Remove card from hand, add to playedCards
        cardIndex = cards.index(ans)
        card = self.hand.pop(cardIndex)
        self._playedCards.append(card)

        return card

    def passMsg(self, msg):
        new_msg = msg.copy()
        new_message['message_type'] = 'info'
        self.sendMessage(msg)

    def printCards(self):
        """Prints 'nice' view of player's hand to console."""
        print('Cards: ', end="")
        cards = []
        for card in self.hand:
            cards.append(card.prettyString())
        print(*cards, sep=", ")
