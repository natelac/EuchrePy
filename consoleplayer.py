from player import Player
import abc


class HumanPlayer(Player, abc.ABC):
    """A Player class that prints to and takes input from the console."""

    def __init__(self, name='Human'):
        Player.__init__(self, name)

    def orderUp(self):
        self.printCards()
        ans = input('Order up? y/n\n')
        return ans == 'y'

    def orderTrump(self):
        ans = input('Call trump? y/n\n')
        return ans == 'y'

    def callTrump(self):
        ans = input('Enter suit to pick\n')
        while ans not in ['C', 'S', 'H', 'D'] and ans != topCard['topCard'].suit:
            ans = input('Not a valid suit.\n')
        return ans

    def goAlone(self):
        ans = input('Go alone? y/n\n')
        return ans == 'y'

    def playCard(self, leader, cardsPlayed, trump):
        # Print trump and cards
        print("Trump Suit:", trump)
        cards = [str(card) for card in self.hand]
        self.printCards()

        # Get card to play from user
        ans = input('Enter card to play\n')
        while ans not in cards:
            ans = input('Not a card in your hand.\n')

        # Remove card from hand, add to playedCards
        cardIndex = cards.index(ans)
        card = self.hand.pop(cardIndex)
        self._playedCards.append(card)

        return card

    def passMsg(self, msg, content=None):
        def points():
            print(
                f"Team1 has {content[0].points} points\tTeam2 has {content[1].points} points")

        def roundResults():
            winningTeam, points, tricks = content
            winners = content[0].getPlayers()
            print("{} and {} win the round with {} points and {} trick taken"
                  .format(winners[0], winners[1], points, tricks))

        def gameResults():
            print("TODO")

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
                   "invalidSuit": invalidSuit,
                   "roundResults": roundResults,
                   "gameResults": gameResults}
        options[msg]()

    def printCards(self):
        """Prints 'nice' view of player's hand to console."""
        print('Cards: ', end="")
        cards = []
        for card in self.hand:
            cards.append(card.prettyString())
        print(*cards, sep=", ")
