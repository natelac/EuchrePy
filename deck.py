import random
from card import Card

class Deck:
    """Deck consisting of 24 cards for the game of Euchre.

    ...

    Attributes
    ----------
    ranks : list
        Contains all possible ranks (str) for the game of Euchre
    suits : list
        Contains all possible suits (str) for the game of Euchre
    cards : list
        Contains every unique card that can be made from ranks and suits

    Methods
    -------
    deal
        Return 5 hands of 4 cards each
    shuffle
        Randomizes the order of the cards in the deck
    print
        Prints every card in the deck's shorthand name
    printFull
        Prints every card in the deck's full name
    """

    ranks = ['Ace','King','Queen','Jack','10','9']
    suits = ['Clubs','Spades','Hearts','Diamonds']
    # shortRanks = ['A','K','Q','J','10','9']
    # shortSuits = ['C','S','H','D']

    def __init__(self):
        self.cards: List[Card] = []
        self.size = 24
        for suit in Deck.suits:
            for rank in Deck.ranks:
                self.cards.append(Card(rank,suit))

    def deal(self) -> tuple:
        """Returns four hands and a kitty selected in order from the deck and an up card.

        Remember to shuffle before you deal if you want to randomize the cards.

        Returns
        -------
        tuple
            First element is a list of list of cards, second element
            is the up card
        """
        hands = [[],[],[],[],[]]
        for i in range(self.size):
            hands[i % 5].append(self.cards[i])
        return hands

    def shuffle(self):
        """Randomizes the order of the cards in the deck."""
        random.shuffle(self.cards)

    def print(self):
        """Prints the cards in the deck using card shorthand, i.e. 'AC'
        for 'Ace of Clubs'.
        """
        for card in self.cards:
            print(card)

    def printFull(self):
        """Prints the cards in the deck using long form, i.e. 'Ace of Clubs'"""
        for card in self.cards:
            print(card.toString())
