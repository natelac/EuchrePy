import random


class Card:
    """Card object used to construct a deck.

    Contains the shorthand names for the rank and suit of a Card.

    Attributes:
        rank (str): The shorthand rank of the card, i.e. 'Ace' is 'A'.
        suit (str): The shorthand suit of the card, i.e. 'Clubs' is 'C'.
    """
    
    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9']
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']

    def __init__(self, rank, suit):
        """
        Args:
            rank (str): Longform rank of card with first character capitalized
            suit (str): Longform suit of card with first character capitalized
        """
        self._rank = str(rank)
        self._suit = str(suit)
        self._off_suit = {
            'C': 'S',
            'S': 'C',
            'H': 'D',
            'D': 'H'
        }
        self._values = {
            'A': 6,
            'K': 5,
            'Q': 4,
            'J': 3,
            '10': 2,
            '9': 1
        }
        self._symbols = {
            'C': '♣',
            'S': '♠',
            'H': '♥',
            'D': '♦'
        }

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    @property
    def rank(self):
        """Shorthand rank of card.

        Returns:
            rank (str): Shorthand rank of the card
        """
        if self._rank == '10':
            return '10'
        else:
            return self._rank[0]

    @property
    def suit(self):
        """Shorthand suit of the Card.

        Returns:
            suit (str): Shorthand suit of the Card
        """
        return self._suit[0]

    def getSuit(self, trump_suit):
        """Shorthand suit of the Card given trump.

        Checks if the card is left bower.

        Returns:
            suit (str): Shorthand suit of the Card given trump
        """
        if self.isLeftBower(trump_suit[0]):
            return self._off_suit[self.suit]
        return self.suit

    @property
    def name(self):
        """Name of the card.

        For example, returns 'Ace of Clubs' for the Ace of Clubs.

        Returns:
            (str): Full name of the Card
        """
        return self._rank + ' of ' + self._suit

    def prettyString(self):
        """A pretty version of the card.

        For example, returns '[ AC ]' for 'Ace of Clubs'.

        Returns:
            (str): Pretty version of the card
        """
        if self.suit in ['D', 'H']:
            # return "\u001b[31m[ " + self.rank[0] + ' ' + self._symbols[self.suit[0]] + " ]\033[0m"
            return "\u001b[31m[ " + self.rank[0] + self.suit[0] + " ]\033[0m"
        else:
            # return "[ " + self.rank[0] + ' ' + self._symbols[self.suit[0]] + " ]"
            return "[ " + self.__str__() + " ]"

    @classmethod
    def str2card(cls, shorthand):
        """Convert shorthand string to card object.

        Args:
            shorthand (str): Shorthand name of the card where the first
                character is the rank and the second is the suit

        Returns:
            (Card): A card object corresponding to the shorthand
        """
        rank = shorthand[0]
        suit = shorthand[1]

        for rank_long in cls.ranks:
            if rank_long[0] == rank:
                rank = rank_long

        for suit_long in cls.suits:
            if suit_long[0] == suit:
                suit = suit_long

        return Card(rank, suit)

    def __str__(self):
        """Shorthand name of card.
        'AC' for 'Ace of Clubs'.

        Returns:
            (str): Shorthand name of card
        """
        return self._rank[0] + self._suit[0]

    def __repr__(self):
        return self.__str__()

    def value(self, led_suit, trump_suit):
        """Value of card in context of the led suit and the trump suit.

        Args:
            led_suit (str): Suit of card led
            trump_suit (str): Trump suit

        Returns:
            (int): Value of card relative to other cards
        """
        val = self._values[self.rank]
        if self.isRightBower(trump_suit[0]):
            return 52
        elif self.isLeftBower(trump_suit[0]):
            return 51
        elif self.suit == trump_suit[0]:
            return val + 6
        elif self.suit == led_suit[0]:
            return val
        else:
            return 0

    def isLeftBower(self, trump_suit):
        """Whether the card is left bower given the trump suit.

        Args:
            trump_suit (str): Trump suit

        Returns:
            (bool): True if left bower, otherwise False
        """
        if self.rank == 'J' and self.suit == self._off_suit[trump_suit[0]]:
            return True
        else:
            return False

    def isRightBower(self, trump_suit):
        """Whether the card is right bower given the trump suit.

        Args:
            trump_suit (str): Trump suit

        Returns:
            (bool): True if right bower, otherwise False
        """
        if self.rank == 'J' and self.suit == trump_suit[0]:
            return True
        else:
            return False
