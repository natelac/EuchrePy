import random
from card import Card


class Deck:
    """Deck consisting of 24 cards for the game of Euchre.

    ...

    Attributes:
        ranks: List containing all possible ranks (str) for the game of Euchre.
        suits: List containing all possible suits (str) for the game of Euchre.
        cards: List containing every unique card that can be made from ranks and suits.
        size: Number of cards in the deck.
    """

    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9']
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']

    def __init__(self):
        self.cards: List[Card] = []
        self.size = 24

        # Construct deck with each card.
        for suit in Deck.suits:
            for rank in Deck.ranks:
                self.cards.append(Card(rank, suit))

    def deal(self):
        """Returns four hands and a kitty selected in order from the deck and an up card.

        Remember to shuffle before you deal if you want to randomize the cards.

        Returns:
            Tuple where first element is a list of list of cards,
                and second element is the up card
        """
        hands = [[], [], [], [], []]
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
