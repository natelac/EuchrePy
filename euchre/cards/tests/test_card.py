import unittest

from euchre import Card


class TestCard(unittest.TestCase):
    
    # All suits and ranks in euchre
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    ranks = ['Ace', 'King', 'Queen', 'Joker', '10', '9']

    # Cards and tuples of their ranks and suits
    card_tups = []
    cards = []
    for suit in suits:
        for rank in ranks:
            card_tups.append((rank, suit))
            cards.append(Card(rank, suit))

    def test_init(self):
        """
        Test card creation.
        """
        for i, tup in enumerate(self.card_tups):
            self.assertEqual(self.cards[i]._rank, tup[0])
            self.assertEqual(self.cards[i]._suit, tup[1])

    def test_get_suit(self):
        """
        Test suit of cards with trump suit.
        """
        trump_suit = 'C'

        for card in self.cards:
            if card.suit == 'S' and card.rank == 'J':
                card_suit = card.getSuit(trump_suit)
                self.assertEqual(card_suit, trump_suit)

    def test_is_left_bower(self):
        """
        Test check for left bower.
        """
        trump_suit = 'H'

        for card in self.cards:
            is_left_bower = card.isLeftBower(trump_suit)
            if card.rank == 'J' and card.suit == 'D':
                self.assertTrue(is_left_bower)
            else:
                self.assertFalse(is_left_bower)

    def test_is_right_bower(self):
        """
        Test check for right bower.
        """
        trump_suit = 'S'

        for card in self.cards:
            is_right_bower = card.isRightBower(trump_suit)
            if card.rank == 'J' and card.suit == 'S':
                self.assertTrue(is_right_bower)
            else:
                self.assertFalse(is_right_bower)

    def test_value(self):
        """
        Test value of cards.
        """
        # Test values against reference card, Queen of Spades
        trump_suit = 'C'
        led_suit = 'S'
        card = Card("Queen", "Spades")
        ref_value = card.value(led_suit, trump_suit)
        
        card_vals = [
                (Card("Ace", "Spades"), True),
                (Card("Jack", "Spades"), True),
                (Card("Jack", "Clubs"), True),
                (Card("9", "Clubs"), True),
                (Card("Jack", "Hearts"), False),
                (Card("10", "Spades"), False),
                (Card("Ace", "Diamonds"), False),
                ]

        for card, truth in card_vals:
            card_value = card.value(led_suit, trump_suit)
            self.assertEqual(card_value > ref_value, truth)

        # Test left and right bower
        left_bower_value = Card("Jack", "Spades").value(led_suit, trump_suit)
        right_bower_value = Card("Jack", "Clubs").value(led_suit, trump_suit)
        self.assertTrue(left_bower_value < right_bower_value)
