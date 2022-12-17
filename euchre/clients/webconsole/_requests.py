"""Methods for getting user input for requests from server.
"""

from euchre.utils import printCards

def orderUp(self):
    printCards(self.game_info['hand'])
    ans = input('Order up? y/n\n')
    if signals['shutdown']:
        print("Server closed")
        return
    self.sendMessage({
        'message_type': 'response',
        'response_type': 'order_up',
        'response': ans
    })

def orderTrump(self):
    ans = input('Call trump? y/n\n')
    if signals['shutdown']:
        print("Server closed")
        return
    self.sendMessage({
        'message_type': 'response',
        'response_type': 'order_trump',
        'response': ans
    })

def callTrump(self):
    ans = input('Enter suit to pick\n')
    while ans not in ['C', 'S', 'H', 'D'] \
            and ans != self.game_info['top_card'].suit:
        ans = input('Not a valid suit.\n')
    if signals['shutdown']:
        print("Server closed")
        return
    self.sendMessage({
        'message_type': 'response',
        'response_type': 'call_trump',
        'response': ans
    })

def goAlone(self):
    ans = input('Go alone? y/n\n')
    if signals['shutdown']:
        print("Server closed")
        return
    self.sendMessage({
        'message_type': 'response',
        'response_type': 'go_alone',
        'response': ans
    })

def playCard(self):
    # Print trump and cards
    print("Trump Suit:", self.game_info['trump'])
    printCards(self.game_info['hand'])

    # Get card to play from user
    cards = [str(card) for card in self.game_info['hand']]
    ans = input('Enter card to play\n')
    while ans not in cards:
        ans = input('Not a card in your hand.\n')

    # Remove card from hand, add to playedCards
    cardIndex = cards.index(ans)
    card = self.game_info['hand'].pop(cardIndex)
    self.game_info['played_cards'].append(card)

    # self._playedCards.append(card)
    if signals['shutdown']:
        print("Server closed")
        return
    self.sendMessage({
        'message_type': 'response',
        'response_type': 'play_card',
        'response': ans
    })

def discardCard(self):
    # Add top card to the hand
    hand = self.game_info['hand']
    top_card = self.game_info['top_card']
    hand.append(top_card)
    printCards(hand)

    # Get card to discard from user
    cards = [str(card) for card in hand]
    ans = input('Enter card to discard:\n')
    while ans not in cards:
        ans = input('Not a card in your hand.\n')

    # Remove and return discard card
    card_index = cards.index(ans)
    discard_card = hand.pop(card_index)

    self.sendMessage({
        'message_type': 'response',
        'response_type': 'discard_card',
        'response': ans
    })
