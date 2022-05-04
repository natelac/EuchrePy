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

    def passMsg(self, msg):
        def points():
            team1, team2 = msg['teams']
            print(f"Team1 has {team1.points} points\tTeam2 has {team2.points} points")

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
            print(f"{msg['leader']} starts the first trick")

        def played():
            print(f"{msg['player']} played {msg['card'].prettyString()}")

        def taker():
            print(f"{msg['taker']} takes the hand")

        def deniedUp():
            print(f"{msg['player']} denied ordering up")

        def deniedTrump():
            print(f"{msg['player']} denied ordering trump")

        def penalty():
            if msg['player'] is self:
                print(
                    f"You reneged by playing {msg['card']} and the opposing team was awarded 2 points")
            else:
                print(
                    f"{msg['player']} reneged by playing {msg['player']} and your team was awarded 2 points")

        def invalidSuit():
            print(
                "Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")

        options = {'points': points,
                   'misdeal': misdeal,
                   'new_leader': leader,
                   'played': played,
                   'new_taker': taker,
                   'denied_up': deniedUp,
                   'denied_trump': deniedTrump,
                   'penalty': penalty,
                   'invalid_suit': invalidSuit,
                   'roundResults': roundResults,
                   'gameResults': gameResults}
        options[msg['type']]()

    def printCards(self):
        """Prints 'nice' view of player's hand to console."""
        print('Cards: ', end="")
        cards = []
        for card in self.hand:
            cards.append(card.prettyString())
        print(*cards, sep=", ")
