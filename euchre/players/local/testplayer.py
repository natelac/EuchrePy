import abc

from euchre.players.player import Player


class TestPlayer(Player, abc.ABC):
    """A Player class that can be fed valid responses to a game.
    """

    def __init__(self, name='AI', cmd_queue=None):
        Player.__init__(self, name)

        # List (queue) of commands to return to game:
        #   'T' = return True
        #   'F' = return False
        #   'AC' = return Ace of Clubs 
        #   Empty list returns BasicAI answer 
        if cmd_queue is None:
            self.cmd_queue = []
        else:
            self.cmd_queue = cmd_queue

    # Decision methods that require a return value
    # -------------------------------------------------------------------------
    def orderUp(self):
        if len(cmd_queue) != 0:
            if cmd_queue[0] not in ['T', 'F']:
                raise ValueError("Must be 'T' or 'F'")
            ans = cmd_queue.pop(0)
            return ans == 'T'
        else:
            return False

    def discardCard(self, top_card):
        if len(cmd_queue) != 0:
            self.hand.append(top_card) # Order matters
            discard_card = cmd_queue.pop(0)
            self.hand.remove(discard_card)
        else:
            # Put an arbitrary card in kitty
            discard_card = self.hand.pop() # Order matters
            self.hand.append(top_card)
        return discard_card

    def orderTrump(self):
        if len(cmd_queue) != 0:
            if cmd_queue[0] not in ['T', 'F']:
                raise ValueError("Must be 'T' or 'F'")
            ans = cmd_queue.pop(0)
            return ans == 'T'
        else:
            return False

    def callTrump(self, up_suit):
        if len(cmd_queue) != 0:
            if cmd_queue[0] not in ['C', 'S', 'H', 'D']:
                raise ValueError("Must be a suit in 'C', 'S', 'H', or 'D'")
            ans = cmd_queue.pop(0)
            return ans
        else:
            return None

    def goAlone(self):
        if len(cmd_queue) != 0:
            if cmd_queue[0] not in ['T', 'F']:
                raise ValueError("Must be 'T' or 'F'")
            ans = cmd_queue.pop(0)
            return ans == 'T'
        else:
            return False

    def playCard(self, leader, cards_played, trump):
        if len(cmd_queue) != 0:
            ans = cmd_queue.pop(0)
            self.hand.remove(ans)
            return ans
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
