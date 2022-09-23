import abc

from euchre.players.player import Player



class ConsolePlayer(Player, abc.ABC):
    """A Player class that prints to and takes input from the console.
    """

    def __init__(self, name='Human'):
        Player.__init__(self, name)
        self.top_card = None

    # Decision methods that require a return value
    # -------------------------------------------------------------------------
    def orderUp(self):
        self.printCards()
        ans = input('Order up? y/n\n')
        return ans == 'y'

    def orderTrump(self):
        ans = input('Call trump? y/n\n')
        return ans == 'y'

    def callTrump(self, topSuit):
        ans = input('Enter suit to pick:\n')
        while ans not in ['C', 'S', 'H', 'D'] and ans != topSuit:
            ans = input('Not a valid suit.\n')
        return ans

    def goAlone(self):
        ans = input('Go alone? y/n\n')
        return ans == 'y'

    def playCard(self, leader, cardsPlayed, trump):
        # Print cards (and trump?)
        #print("Trump Suit:", trump)
        cards = [str(card) for card in self.hand]
        self.printCards()

        # Get card to play from user
        ans = input('Enter card to play:\n')
        while ans not in cards:
            ans = input('Not a card in your hand.\n')

        # Remove card from hand, add to playedCards
        card_index = cards.index(ans)
        card = self.hand.pop(card_index)

        return card

    def discardCard(self, top_card):
        # Add top card to the hand
        self.hand.append(top_card)
        self.printCards()

        # Get card to discard from user
        cards = [str(card) for card in self.hand]
        ans = input('Enter card to discard:\n')
        while ans not in cards:
            ans = input('Not a card in your hand.\n')

        # Remove and return discard card
        card_index = cards.index(ans)
        discard_card = self.hand.pop(card_index)

        return discard_card

    # Information updates that don't require a return value
    # -------------------------------------------------------------------------
    def updateHand(self, cards):
        self.hand = cards

    def pointsMsg(self, team1, team2):
        print()
        print(f"{team1._p1}, {team1._p2} have {team1.points} points\t {team2._p1}, {team2._p2} have {team2.points} points")
        print('-'*50)

    def dealerMsg(self, dealer):
        print(f"The dealer is {dealer}")

    def topCardMsg(self, top_card):
        self.top_card = top_card
        print(f"The top card is {top_card.prettyString()}")

    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        winners = taking_team.getPlayers()
        print("{} and {} win the round with {} points and {} trick taken"
              .format(winners[0], winners[1],
                      points_scored, team_tricks))

    def orderUpMsg(self, player, top_card):
        print(f"{player} ordered up {top_card}")

    def deniedUpMsg(self, player):
        print(f"{player} denied ordering up")

    def orderedTrumpMsg(self, player, trump_suit):
        print(f"{player} chose {trump_suit} as the trump suit")

    def deniedTrumpMsg(self, player):
        print(f"{player} denied ordering trump")

    def gameResultsMsg(self):
        print("TODO")

    def misdealMsg(self):
        print("Misdeal, new dealer")

    def leaderMsg(self, leader):
        print(f"{leader} starts the first trick")

    def playedMsg(self, player, card):
        print(f"{player} played {card.prettyString()}")

    def takerMsg(self, taker):
        print(f"{taker} takes the hand")

    def penaltyMsg(self, player, card):
        if player is self:
            print(
                f"You reneged by playing {card}")
        else:
            print(
                f"{player} reneged by playing {card}")

    def invalidSuitMsg(self):
        print(
                "Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")

    def trickStartMsg(self):
        print()

    def newTrumpMsg(self, trump_suit):
        pass
