from player import Player
import abc


class HumanPlayer(Player, abc.ABC):
    def __init__(self, name='Human'):
        Player.__init__(self, name)

    def orderUp(self, orderInfo):
        self.printCards()
        ans = input('Order up? y/n\n')
        return ans == 'y'

    def orderTrump(self, orderInfo):
        ans = input('Call trump? y/n\n')
        if ans == 'y':
            return True
        else:
            return False

    def callTrump(self, orderInfo):
        """
        Need to implement so user cannot pick top card as trump
        """
        ans = input('Enter suit to pick\n')
        while ans not in ['C', 'S', 'H', 'D'] and ans != orderInfo['topCard'].suit:
            ans = input('Not a valid suit.\n')
        return ans

    def goAlone(self):
        ans = input('Go alone? y/n\n')
        return ans == 'y'

    def playCard(self, leader, cardsPlayed, trump):
        cards = [str(card) for card in self.hand]
        # print(cardsPlayed)
        print("Trump Suit:", trump)
        self.printCards()
        ans = input('Enter card to play\n')
        while ans not in cards:
            ans = input('Not a card in your hand.\n')
        cardIndex = cards.index(ans)
        card = self.hand.pop(cardIndex)
        self._playedCards.append(card)
        return card

    def passMsg(self, msg, content=None):
        """Messages are directly printed
        """

        def points():
            print(
                f"Team1 has {content[0].points} points\tTeam2 has {content[1].points} points")

        def misdeal():
            print("Misdeal, new dealer")

        def leader():
            print(f"{content} starts the first trick")

        def played():
            print(f"{content[0]} played {content[1].prettyString()}")

        def taker():
            print(f"{content} takes the hand")

        def deniedUp():
            print(f"{content} denied ordering up")

        def deniedTrump():
            print(f"{content} denied ordering trump")

        def penalty():
            if content[0] is self:
                print(
                    f"You reneged by playing {content[1]} and your team was penalized 4 points")
            else:
                print(
                    f"{content[0]} reneged by playing {content[1]} and their team was penalized 4 points")

        def invalidSuit():
            print(
                "Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")
        options = {"points": points,
                   "misdeal": misdeal,
                   "leader": leader,
                   "played": played,
                   "taker": taker,
                   "deniedUp": deniedUp,
                   "deniedTrump": deniedTrump,
                   "penalty": penalty,
                   "invalidSuit": invalidSuit}
        options[msg]()

    def printCards(self):
        print('Cards: ', end="")
        cards = []
        for card in self.hand:
            cards.append(card.prettyString())
        print(*cards, sep=", ")
