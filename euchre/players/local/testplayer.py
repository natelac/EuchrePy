import abc

from euchre.players.player import Player
from euchre.cards.card import Card


class TestPlayer(Player, abc.ABC):
    """A Player class that can be fed valid responses to a game.
    """

    def __init__(self, name='AI', commands=None, debug=False):
        Player.__init__(self, name)

        self.debug = debug

        # List (queue) of commands to return to game:
        #   'T' = return True
        #   'F' = return False
        #   'AC' = return Ace of Clubs 
        #   Empty list returns BasicAI answer 
        if commands is None:
            self.commands = []
        else:
            self.commands = commands


    def dprint(self, *args):
        if self.debug:
            print(*args)

    # Decision methods that require a return value
    # -------------------------------------------------------------------------
    def orderUp(self):

        self.dprint(self.name, 'asked to order up')

        if len(self.commands) != 0:
            if self.commands[0] not in ['y', 'n']:
                raise ValueError(f"Must be 'y' or 'n', got '{self.commands[0]}'")
            ans = self.commands.pop(0)

            self.dprint(self.name, 'answered', ans)

            return ans == 'y'

        else:
            return False

    def discardCard(self, top_card):
        self.dprint(self.name, 'asked to discard')
        if len(self.commands) != 0:
            self.dprint(self.name, 'has cards', self.hand, 
                       'and is looking to discard', self.commands[0])
            self.hand.append(top_card) # Order matters
            discard_card_str = self.commands.pop(0)
            discard_card = Card.str2card(discard_card_str)
            self.hand.remove(discard_card)
        else:
            # Put an arbitrary card in kitty
            discard_card = self.hand.pop() # Order matters
            self.hand.append(top_card)

        return discard_card

    def orderTrump(self):
        if len(self.commands) != 0:
            if self.commands[0] not in ['y', 'n']:
                raise ValueError(f"Must be 'y' or 'n', got '{self.commands[0]}'")
            ans = self.commands.pop(0)
            return ans == 'y'
        else:
            return False

    def callTrump(self, up_suit):
        if len(self.commands) != 0:
            if self.commands[0] not in ['C', 'S', 'H', 'D']:
                raise ValueError(f"Must be a suit in 'C', 'S', 'H', or 'D', got '{self.commands[0]}'")
            ans = self.commands.pop(0)
            return ans
        else:
            return None

    def goAlone(self):
        if len(self.commands) != 0:
            if self.commands[0] not in ['y', 'n']:
                raise ValueError(f"Must be 'y' or 'n', got '{self.commands[0]}'")
            ans = self.commands.pop(0)
            return ans == 'y'
        else:
            return False

    def playCard(self, leader, cards_played, trump):
        if len(self.commands) != 0:
            self.dprint(self.name, 'has cards:', self.hand)
            self.dprint(self.name, 'is is playing', self.commands[0])
            card_str = self.commands.pop(0)
            card = Card.str2card(card_str)
            self.hand.remove(card)
            return card
        else:
            # Play an arbitrary card if player is leader
            if leader is self:
                card = self.hand.pop()
            else:
                # Play an arbitrary valid card
                leadSuit = cards_played[leader][-1].suit
                playable = [card for card in self.hand if card.getSuit(
                    trump) == leadSuit]
                card = playable[0] if playable else self.hand[0]
                self.hand.remove(card)
            return card

    # Information updates that don't require a return value
    # -------------------------------------------------------------------------
    def updateHand(self, cards):
        self.hand = cards

    def pointsMsg(self, team1, team2):
        pass

    def dealerMsg(self, dealer):
        pass

    def topCardMsg(self, top_card):
        pass

    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        pass

    def orderUpMsg(self, player, top_card):
        pass

    def deniedUpMsg(self, player):
        pass

    def orderedTrumpMsg(self, player, trump_suit):
        pass

    def deniedTrumpMsg(self, player):
        pass

    def gameResultsMsg(self, winning_team):
        pass

    def misdealMsg(self):
        pass

    def leaderMsg(self, leader):
        pass

    def playedMsg(self, player, card):
        pass

    def takerMsg(self, taker):
        pass

    def penaltyMsg(self, player, card):
        pass

    def invalidSuitMsg(self):
        pass

    def trickStartMsg(self):
        pass

    def newTrumpMsg(self, trump):
        pass
