import random

from .card import Card


class Deck:
    """Deck consisting of 24 cards for the game of Euchre.

    Attributes:
        ranks (list): All possible ranks (str) for the game of Euchre
        suits (list): All possible suits (str) for the game of Euchre
        cards (list): Every unique card that can be made from ranks and suits
        size (int): Number of cards in the deck
    """

    # Full names of ranks and suits
    suits = Card.suits
    ranks = Card.ranks

    # Preset deals for testing
    #   'balanced':
    #       Attempts to get the win-rate of picking arbitrary cards close
    #       to 50%. The dealer decides to discard clubs or diamonds which
    #       benefits either their team or the opposing team. based on play
    #       order where first hand is left of dealer
    raw_preset_decks = {
            'balanced':
                 [['JC', 'AD', 'QC', 'KD', 'QH'],
                  ['AS', 'QD', 'AC', 'KH', 'KC'],
                  ['KS', '9D', '9C', 'AH', '1S'],
                  ['JS', '1D', '1C', '1H', '9H'],
                  ['9S', 'QS', 'JH', 'JD']],
            }

    # Convert each string to card
    preset_decks = dict()
    for k, hands in raw_preset_decks.items():
        new_hands = []
        for hand in hands:
            new_hand = []
            for card in hand:
                new_hand.append(Card.str2card(card))
            new_hands.append(new_hand)
        preset_decks[k] = new_hands

    def __init__(self, deck_preset=None):
        self.cards: List[Card] = []
        self.size = 24
        self.disable_shuffle = False
        self.deck_preset = deck_preset

        # Construct deck with each card.
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(rank, suit))

    def deal(self):
        """Deals four hands and a kitty selected in order from the deck
        and an up card.

        Remember to shuffle before you deal if you want to randomize the cards.

        Returns:
            hands (tuple): First element is a list of list of cards
                and second element is the up card
        """
        if self.deck_preset:
            return self.preset_decks[self.deck_preset].copy()
        hands = [[], [], [], [], []]
        for i in range(self.size):
            hands[i % 5].append(self.cards[i])
        return hands

    def shuffle(self):
        """Randomizes the order of the cards in the deck.
        """
        if self.disable_shuffle:
            return
        random.shuffle(self.cards)

    def print(self):
        """Prints the cards in the deck using card shorthand, i.e. 'AC'
        for 'Ace of Clubs'.
        """
        for card in self.cards:
            print(card)

    def printFull(self):
        """Prints the cards in the deck using long form, i.e. 'Ace of Clubs'
        """
        for card in self.cards:
            print(card.toString())

