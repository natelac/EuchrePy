import random


class Card:
    """Card object used to construct a deck

    Attributes:
        rank: The shorthand rank of the card, i.e. 'Ace' is 'A'
        suit: The shorthand suit of the card, i.e. 'Clubs' is 'C'.
    """

    def __init__(self, rank: str, suit: str):
        """Inits Card"""
        self._rank: str = rank
        self._suit: str = suit
        self._offSuit: dict = {
            'C': 'S',
            'S': 'C',
            'H': 'D',
            'D': 'H'
        }
        self._values: dict = {
            'A': 6,
            'K': 5,
            'Q': 4,
            'J': 3,
            '10': 2,
            '9': 1
        }
        self._symbols: dict = {
            'C': '♣',
            'S': '♠',
            'H': '♥',
            'D': '♦'
        }

    @property
    def rank(self):
        "Shorthand rank of card"
        if self._rank == '10':
            return '10'
        else:
            return self._rank[0]

    @property
    def suit(self):
        "Shorthand suit of card"
        return self._suit[0]

    def getSuit(self, trumpSuit):
        """Returns suit of card in context of trump suit"""
        if self.isLeftBower(trumpSuit):
            return self._offSuit[self.suit]
        return self.suit

    def __str__(self) -> str:
        """Returns shortened name of card, i.e. 'AC' for 'Ace of Clubs'.
        NOTE: '10 of Clubs' would be 1C"""
        return self._rank[0] + self._suit[0]

    def value(self, ledSuit, trumpSuit):
        """Returns value of card in the context of a tricksTaken"""
        val = self._values[self.rank]
        if self.isRightBower(trumpSuit):
            return 52
        elif self.isLeftBower(trumpSuit):
            return 51
        elif self.suit == trumpSuit:
            return val + 6
        elif self.suit == ledSuit:
            return val
        else:
            return 0

    def isLeftBower(self, trumpSuit):
        "Returns whether the card is left bower given the trump suit."
        if self.rank == 'J' and self.suit == self._offSuit[trumpSuit]:
            return True
        else:
            return False

    def isRightBower(self, trumpSuit):
        "Returns whether the card is right bower given the trump suit."
        if self.rank == 'J' and self.suit == trumpSuit:
            return True
        else:
            return False

    def toString(self) -> str:
        """Returns the full name of a card, for example 'Ace of Clubs'.

        Implicitly cast the card object to string if you want shorthand,
        i.e. 'AC' for 'Ace of Clubs'"""
        return self._rank + ' of ' + self._suit

    def prettyString(self):
        """Returns a pretty version of the card,
        i.e. '[ AC ]' for 'Ace of Clubs'
        """
        if self.suit in ['D', 'H']:
            return "\u001b[31m[ " + self.rank[0] + self.suit[0] + " ]\033[0m"
        else:
            return "[ " + self.__str__() + " ]"
