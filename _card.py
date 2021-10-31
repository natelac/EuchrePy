import random

class Card:
    """Card object used to construct a deck"""
    def __init__(self, rank: str, suit: str):
        """
        Parameters
        ----------
        rank: str
            The rank of the card, i.e. 'Ace'. Truncated on return
        suit: str
            The suit of the card, i.e. 'Clubs'. Truncated on return
        """
        self._rank: str = rank
        self._suit: str = suit
        self._offSuit: dict = {
            'C':'S',
            'S':'C',
            'H':'D',
            'D':'H'
        }
        self._values: dict = {
            'A':6,
            'K':5,
            'Q':4,
            'J':3,
            '10':2,
            '9':1
        }
        self._symbols: dict = {
            'C':'♣',
            'S':'♠',
            'H':'♥',
            'D':'♦'
        }

    @property
    def rank(self):
        if self._rank == '10':
            return '10'
        else:
            return self._rank[0]

    @property
    def suit(self):
        return self._suit[0]

    def getSuit(self, trump):
        if self._isLeftBower(trump):
            return self._offSuit[self.suit]
        return self.suit

    def __str__(self) -> str:
        """
        Returns
        -------
        string
            A string representing the cards rank and suit,
            i.e. 'AC' for 'Ace of Clubs'. Note '10 of Clubs' would be 1C
        """
        # if self.rank == '10':
        #     return '10' + self.suit[0]
        # else:
        #     return self.rank[0] + self.suit[0]
        return self._rank[0] + self._suit[0]

    def value(self, ledSuit, trumpSuit):
        val = self._values[self.rank]
        if self._isRightBower(trumpSuit):
            return 52
        elif self._isLeftBower(trumpSuit):
            return 51
        elif self.suit == trumpSuit:
            return val + 6
        elif self.suit == ledSuit:
            return val
        else:
            return 0

    def _isLeftBower(self, trumpSuit):
        if self.rank == 'J' and self.suit == self._offSuit[trumpSuit]:
            return True
        else:
            return False

    def _isRightBower(self, trumpSuit):
        if self.rank == 'J' and self.suit == trumpSuit:
            return True
        else:
            return False

    def toString(self) -> str:
        """Returns the full name of a card, for example 'Ace of Clubs'.

        Implicitly cast the card object to string if you want shorthand,
        i.e. 'AC' for 'Ace of Clubs'

        Returns
        -------
        str
            Full name of a card, for example 'Ace of Clubs'
        """
        return self._rank + ' of ' + self._suit

    def prettyString(self):
        if self.suit in ['D','H']:
            return "\u001b[31m[ " + self.rank[0] + self.suit[0] + " ]\033[0m"
        else:
            return "[ " + self.__str__() + " ]"
