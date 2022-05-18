# import numpy as np
# from cards.deck import Deck
#
# game_state = {
#     'deck': Deck()
#     'teams':
#         {
#         'players':, # player_ids of 2 players on team
#         'score':,
#         'are_makers', # bool for if this team is the makers
#         }
#     'phase':, # 'deal', 'ordering_up', 'ordering_trump', 'play'
#     'turn':, # % 4 for index of player whos turn it is. There are 4 x 5 = 20 turns
#     'table': [] # list of player_ids where the last (3rd) index is the dealer
#     'up_card':, # Card turned up, important when selecting ordering up/selecting trump
#     'ordered_up':, # bool for if the card was ordered up
#     'trump_suit':, #
#     'alone_player':, # index of player going alone
# }
#
# class StandardGame:
#     """Standard game of euchre
#     Source: https://en.wikipedia.org/wiki/Euchre
#     """
#
#     def __init__(self, players):
#         """Initialize game with first and last 2 players on teams with eachother
#         """
#         self.game_info = {
#             'deck': Deck(),
#             'teams':
#                 {
#                 'players': player_ids[:2],
#                 'score': 0,
#                 'are_makers': False
#                 },
#             'phase': 'deal',
#             'turn': 0,
#             'table': [players[0], players[2], players[1], players[3]],
#             'ordered_up': False,
#             'up_card': None,
#             'trump_suit': None,
#             'alone_player': None
#         }
#
#     def play(self):
#         """Plays a game of euchre until a team reaches 10 points."""
#         while not self.getWinningTeam:
#
#
#
#     def getWinningTeam(self):
#         for team in self.game_info['teams']:
#             if team['score'] >= 10:
#                 return team
#         return None # Return None for no winner
#
#     def msgPlayers()
