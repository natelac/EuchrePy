from players.player import Player
import abc


class ConsolePlayer(Player, abc.ABC):
    """A Player class that prints to and takes input from the console."""

    def __init__(self, name='Human'):
        Player.__init__(self, name)

    def updateHand(self, cards):
        self.hand = cards

    def orderUp(self):
        self.printCards()
        ans = input('Order up? y/n\n')
        return ans == 'y'

    def orderTrump(self):
        ans = input('Call trump? y/n\n')
        return ans == 'y'

    def callTrump(self, topSuit):
        ans = input('Enter suit to pick\n')
        while ans not in ['C', 'S', 'H', 'D'] and ans != topSuit:
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
            print()
            print(f"{team1._p1}, {team1._p2} have {team1.points} points\t {team2._p1}, {team2._p2} have {team2.points} points")
            print('-'*50)

        def dealer():
            print(f"The dealer is {msg['player']}")

        def topCard():
            print(f"The top card is {msg['top_card'].prettyString()}")

        def roundResults():
            winners = msg['taking_team'].getPlayers()
            print("{} and {} win the round with {} points and {} trick taken"
                  .format(winners[0], winners[1],
                          msg['points_scored'], msg['team_tricks']))

        def orderedUp():
            print(f"{msg['player']} ordered up {msg['top_card']}")

        def deniedUp():
            print(f"{msg['player']} denied ordering up")

        def orderedTrump():
            print(f"{msg['player']} chose {msg['trump_suit']} as the trump suit")

        def deniedTrump():
            print(f"{msg['player']} denied ordering trump")

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

        def penalty():
            #TODO: Check if other player is teammate
            if msg['player'] is self:
                print(
                    f"You reneged by playing {msg['card']} and the opposing team was awarded 2 points")
            else:
                print(
                    f"{msg['player']} reneged by playing {msg['player']} and your team was awarded 2 points")

        def invalidSuit():
            print(
                "Must call valid suit ['C','S','H','D'] that does not match the suit of the top card")

        def trickStart():
            #TODO:
            print()

        options = {'points': points,
                   'misdeal': misdeal,
                   'new_leader': leader,
                   'card_played': played,
                   'new_taker': taker,
                   'denied_up': deniedUp,
                   'denied_trump': deniedTrump,
                   'penalty': penalty,
                   'invalid_suit': invalidSuit,
                   'round_results': roundResults,
                   'gameResults': gameResults,
                   'top_card': topCard,
                   'ordered_up': orderedUp,
                   'ordered_trump': orderedTrump,
                   'trick_start': trickStart,
                   'dealer': dealer}
        options[msg['type']]()

    def printCards(self):
        """Prints 'nice' view of player's hand to console."""
        print('Cards: ', end="")
        cards = []
        for card in self.hand:
            cards.append(card.prettyString())
        print(*cards, sep=", ")
