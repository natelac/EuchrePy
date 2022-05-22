from euchre.players import WebPlayer
import abc

class ConsoleWebPlayer(WebPlayer, abc.ABC):
    """A Player class that prints to and takes input from the console."""

    def __init__(self, updates, host='localhost', port=6001, name='WebPlayer'):
        WebPlayer.__init__(self, updates, host='localhost',
                           port=6001, name='WebPlayer')

    def updateHand(self, cards):
        self.hand = cards

        msg = {'message_type': 'update_hand',
               'new_hand': [str(card) for card in cards]}
        self.sendMessage(msg)

    def orderUp(self):
        ans = self.request('order_up')
        return ans == 'y'

    def orderTrump(self):
        ans = self.request('order_trump')
        return ans == 'y'

    def callTrump(self, topSuit):
        ans = self.request('call_trump')
        while ans not in ['C', 'S', 'H', 'D'] and ans != topSuit:
            #TODO: Update player they played an invalid suit
            ans = self.request('call_trump')
        return ans

    def goAlone(self):
        ans = self.request('go_alone')
        return ans == 'y'

    def playCard(self, leader, cardsPlayed, trump):
        # Get card to play from user
        ans = self.request('play_card')
        while ans not in cards:
            #TODO: Update player that they played a card not in their hand
            ans = self.request('play_card')

        # Remove card from hand, add to playedCards
        cardIndex = cards.index(ans)
        card = self.hand.pop(cardIndex)
        self._playedCards.append(card)

        return card

    def pointsMsg(self, team1, team2):
        msg = {
                'message_type': 'info',
                'info_type': 'points',
                'team1': {
                    'players': (str(team1._p1), str(team1._p2)),
                    'points': team1.points
                    },
                'team2': {
                    'players': (str(team2._p1), str(team2._p2)),
                    'points': team2.points
                    }
                }
        self.sendMessage(msg)
                
    def dealerMsg(self, dealer):
        msg = {
                'message_type': 'info',
                'info_type': 'dealer',
                'dealer': str(dealer)
                }
        self.sendMessage(msg)

    def topCardMsg(self, top_card):
        msg = {
                'message_type': 'info',
                'info_type': 'top_card',
                'top_card': str(top_card)
                }
        self.sendMessage(msg)

    def roundResultsMsg(self, taking_team, points_scored,
                        team_tricks):
        winners = taking_team.getPlayers()
        msg = {
                'message_type': 'info',
                'info_type': 'round_results',
                'winners': (str(winners[0]), str(winners[1])),
                'points_scored': points_Scored,
                'tricks_taken': team_tricks
                }
        self.sendMessage(msg)

    def orderedUpMsg(self, player, top_card):
        msg = {
                'message_type': 'info',
                'info_type': 'ordered_up',
                'orderer': str(player),
                'top_card': str(top_card)
                }
        self.sendMessage(msg)

    def deniedUpMsg(self, player):
        msg = {
                'message_type': 'info',
                'info_type': 'denied_up',
                'denier': str(player)
                }
        self.sendMessage(msg)

    def orderedTrumpMsg(self, player, trump_suit):
        msg = {
                'message_type': 'info',
                'info_type': 'ordered_trump',
                'orderer': str(player),
                'trump_suit': trump_suit
                }
        self.sendMessage(msg)

    def deniedTrumpMsg(self, player):
        msg = {
                'message_type': 'info',
                'info_type': 'denied_trump',
                'denier': str(player)
                }
        self.sendMessage(msg)

    def gameResultsMsg(self):
        msg = {
                'message_type': 'todo'
                }
        self.sendMessage(msg)

    def misdealMsg(self):
        msg = {
                'message_type': 'info',
                'info_type': 'misdeal'
                }
        self.sendMessage(msg)

    def leaderMsg(self, leader):
        msg = {
                'message_type': 'info',
                'info_type': 'leader',
                'leader': str(leader)
                }
        self.sendMessage(msg)

    def playedMsg(self, player, card):
        msg = {
                'message_type': 'info',
                'info_type': 'played_card',
                'player': str(player),
                'card': str(card)
                }
        self.sendMessage(msg)

    def takerMsg(self, taker):
        msg = {
                'message_type': 'info',
                'info_type': 'taker',
                'taker': taker
                }
        self.sendMessage(msg)

    def penaltyMsg(self, player, card):
        msg = {
                'message_type': 'info',
                'info_type': 'renege',
                'player': str(player),
                'card': str(card)
                }
        self.sendMessage(msg)

    def invalidSuitMsg(self):
        msg = {
                'message_type': 'info',
                'info_type': 'invalid_suit'
                }
        self.sendMessage(msg)

    def trickStartMsg(self):
        msg = {
                'message_type': 'info',
                'info_type': 'trick_start'
                }
        self.sendMessage(msg)

    def newTrumpMsg(self):
        msg = {
                'message_type': 'info',
                'info_type': 'new_trump'
                }
        self.sendMessage(msg)
