import numpy as np
import json

from euchre.cards import Card
from euchre.cards import Deck
from euchre.players import Player


class StandardGame:
    """Standard game of euchre

    Source: https://en.wikipedia.org/wiki/Euchre

    Args:
        team1, team2 (Team): Teams to seat around table, players on same team
                are seated opposite of each other
        log_file (path): Path to of file to log to, default is None which means
                no logging
    """

    def __init__(self, team1, team2, log_file=None):
        # Game info
        self.deck = Deck()
        self.oppo_team = {team1: team2, team2: team1}

        # Game state
        self.gs = {
            'players': [], # List of players, initially equivelant to self.gs['table']
            'teams': (team1, team2),
            'table': [], # Ordered players where index 3 is dealer
            'play_order': [], # Ordered players where index 0 is leader
            'trick_play_orders': None,
            'kitty': [],
            'maker': None,
            'trump': None,
            'top_card': None,
            'going_alone': None,
            'cards_played': None,
            'tricks_taken': None,
            'leader_list': None,
            'renegers': None,
            'takers': None,
        }

        # Randomly seat players around the table
        self.seatPlayers()

        # File to log to
        self.log_file = log_file

    def play(self):
        """Plays a game of euchre until a team reaches 10 points.
        """
        if len(self.gs['players']) != 4:
            raise AssertionError(f"Euchre requires 4 players to play")

        # Game loop
        while not self.getWinner():

            # Inform players of current game state
            for p in self.gs['players']: p.pointsMsg(*self.gs['teams'])
            for p in self.gs['players']: p.dealerMsg(self.gs['table'][3])

            # Enter dealing phase
            maker_selected = self.dealPhase()

            if maker_selected:
                # Enter playing stage
                self.playTricks()
            else:
                # Inform players about misdeal
                for p in self.gs['players']: p.misdealMsg()

            # Save game state
            self.logGameState(maker_selected)

            # Update dealer
            self.updateTableOrder()

        winning_team = self.getWinner()
        if winning_team:
            for p in self.gs['players']: p.gameResultsMsg(winning_team)

    def dealPhase(self):
        """Deals cards and determines trump.

        Returns:
            (bool): True if there was a misdeal, False otherwise.
        """
        # Distribute Cards
        self.deck.shuffle()
        hands = self.deck.deal()
        self.gs['kitty'] = hands[4]
        self.gs['top_card'] = self.gs['kitty'].pop(0)
        for i in range(4):
            self.gs['play_order'][i].updateHand(hands[i])
        for p in self.gs['players']: p.topCardMsg(self.gs['top_card'])

        # Ask players to order up
        all_passed = self.orderPhase()

        # Everyone passed ordering up
        if all_passed:
            # Ask players to order trump
            all_passed = self.trumpPhase()

        return not all_passed

    def orderPhase(self):
        """Asks all players if they want to order up the top card.

        Returns:
            (bool): True if everyone passes ordering up, otherwise False.
        """
        for player in self.gs['table']:
            # Ask players if they want to order up top card
            order_up = player.orderUp()

            # Someone ordered up
            if order_up:
                # Update game state and inform players
                self.gs['maker'] = player
                self.gs['trump'] = self.gs['top_card'].suit
                for p in self.gs['players']:
                    if p is not self.gs['maker']:
                        p.orderUpMsg(self.gs['maker'], self.gs['top_card'])
                for p in self.gs['players']:
                    p.newTrumpMsg(self.gs['trump'])

                # Have dealer discard a card
                discard_card = self.gs['table'][3].discardCard(self.gs['top_card'])
                self.gs['kitty'].append(discard_card)
                return False

            # Inform players that player denied up
            for p in self.gs['players']: p.deniedUpMsg(player)
        return True

    def trumpPhase(self):
        """Asks all players if they want to order trump.

        Returns:
            (bool): True if everyone passes ordering trump, otherwise False.
        """
        # Ask players if they want to call trump
        for player in self.gs['table']:
            order_trump = player.orderTrump()

            # Player calls trump
            if order_trump:
                call = player.callTrump(self.gs['top_card'].suit)

                # Require valid trump that isn't top card suit
                while not self.validTrump(call):
                    player.invalidSuitMsg()
                    call = player.callTrump(self.gs['top_card'].suit)

                # Update game state and inform players
                self.gs['maker'] = player
                self.gs['trump'] = call
                for p in self.gs['players']:
                    if p is not self.gs['maker']:
                        p.orderedTrumpMsg(self.gs['maker'], self.gs['trump'])
                for p in self.gs['players']:
                    p.newTrumpMsg(self.gs['trump'])
                return False

            # Player denies trump
            else:
                for p in self.gs['players']: p.deniedTrumpMsg(player)
        return True

    def playTricks(self):
        """Plays 5 tricks.
        """
        # Initialize trick information
        going_alone = self.gs['maker'].goAlone()
        cards_played = {} # Maps player to cards played
        tricks_taken = {} # Maps players to tricks taken
        takers = [] # Who took what trick, ordered by trick number
        trick_play_orders = []  # Order that tricks are played

        # Initialize cards_played and tricks_taken
        # Skip teammate of player going alone
        if going_alone:
            for player in self.gs['play_order']:
                if self.gs['maker'].getTeammate() is not player:
                    cards_played[player] = []
                    tricks_taken[player] = 0
        else:
            cards_played = {player: [] for player in self.gs['play_order']}
            tricks_taken = {player: 0 for player in self.gs['play_order']}

        # Init taker to player left of dealer
        taker = self.gs['table'][0]

        # Init list of leaders for each trick
        leader_list = []
        for p in self.gs['players']: p.leaderMsg(taker)

        # Play tricks
        for j in range(5):

            # Taker of previous round leads
            leader_list.append(taker)
            self.updatePlayOrder(taker)

            # Inform players of trick start
            for p in self.gs['players']: p.trickStartMsg()

            # Play a trick
            for player in self.gs['play_order']:
                if going_alone and self.gs['maker'].getTeammate() is player:
                    # Skip teammate of player going alone
                    continue
                card = player.playCard(taker, cards_played, self.gs['trump'])
                cards_played[player].append(card)
                for p in self.gs['players']:
                    if p is not player:
                        p.playedMsg(player, card)


            # Decide Taker
            trick = {player: cards[j] for player, cards in cards_played.items()}
            led_suit = trick[taker].suit
            taker = max(trick,
                        key=lambda player: trick[player].value(
                            led_suit, self.gs['trump']))
            for p in self.gs['players']: p.takerMsg(taker)
            tricks_taken[taker] += 1
            takers.append(taker)
            trick_play_orders.append(self.gs['play_order'][:])

        # Penalize any players that reneged, otherwise score round normally
        renegers = self.checkForReneges(leader_list, cards_played, going_alone)
        if renegers:
            self.penalize(renegers, going_alone)
        else:
            self.scoreRound(tricks_taken, going_alone)

        # Log game state
        self.gs['going_alone'] = going_alone
        self.gs['cards_played'] = cards_played
        self.gs['tricks_taken'] = tricks_taken
        self.gs['leader_list'] = leader_list
        self.gs['renegers'] = renegers
        self.gs['takers'] = takers
        self.gs['trick_play_orders'] = trick_play_orders

    def validTrump(self, suit):
        """Checks if a trump call is valid.

        A trump call is valid if it is a valid suit and isn't the same suit
        as the top card.

        Args:
            suit (str): The suit that a player has called.

        Returns:
            (bool): True if the trump is valid, otherwise False.
        """
        if not suit in ['C', 'S', 'H', 'D']:
            return False
        return suit != self.gs['top_card'].suit

    def scoreRound(self, tricks_taken, going_alone):
        """Messages players winner and points won.

        Args:
            tricks_taken (dict): Tricks taken by team
            going_alone (bool): Whether the maker went alone
        """
        # Count tricks taken per team
        team_tricks = {team: 0 for team in self.gs['teams']}
        for player, taken in tricks_taken.items():
            team_tricks[player.team] += taken
        teaking_team = max(team_tricks, key=team_tricks.get)

        # Figure out points
        points = 1
        if self.gs['maker'] in teaking_team.players:
            if going_alone and team_tricks[teaking_team] == 5:
                points = 4
            elif team_tricks[teaking_team] == 5:
                points = 2
        else:
            points = 2

        # Finalize results
        teaking_team.points += points
        for p in self.gs['players']:
            p.roundResultsMsg(teaking_team, points, team_tricks[teaking_team])

    def penalize(self, renegers, going_alone):
        """Penalizes the renegers.

        Penalizes the team only once even if player(s) renege multiple times.
        Penalizes twice as much when a player is going alone.
        Doesn't penalize anyone if both teams renege.

        Args:
            renegers (list): Players to be penalized
        """
        # Use sets to figure out teams to give points to,
        #   if both teams renege no one gets points
        reneging_teams = {player.team for player in renegers}
        teams = {team for team in self.gs['teams']}
        for team in teams - reneging_teams:
            if going_alone:
                team.points += 4
            else:
                team.points += 2

    def checkForReneges(self, leader_list, cards_played, going_alone):
        """Figures out who reneged.

        Args:
            leader_list (list): Players ordered by when they lead the trick
            cards_played (dict): Maps players to a list of cards played.
                    The list of cards is ordered by trick
            going_alone (bool): Whether the maker went alone

        Returns:
            renegers (list): Players that reneged and need to be penalized.
        """
        renegers = []

        # Check each trick for reneges
        for j in range(5):
            leader = leader_list[j]
            leadSuit = cards_played[leader][j].getSuit(self.gs['trump'])

            # Add player to renengers if invalid card played
            for player in self.gs['table']:

                # Skip teammate if going alone
                if going_alone and self.gs['maker'].getTeammate() is player:
                    continue

                # Check for reneges
                cards = cards_played[player][j:]
                playable = [card for card in cards if card.getSuit(
                    self.gs['trump']) == leadSuit]
                if (len(playable) != 0) and (cards[0] not in playable):

                    # Inform players that they reneged
                    for p in self.gs['players']: p.penaltyMsg(player, cards[0])
                    renegers.append(player) if player not in renegers else None

        return renegers

    def seatPlayers(self):
        """Seats the players randomly around table (preserving teams).

        Modifies:
            self.gs['players']
            self.gs['table']
            self.gs['play_order']
        """
        self.gs['players'] = []
        t1 = self.gs['teams'][0].players
        t2 = self.gs['teams'][1].players

        # Shuffle within each team
        np.random.shuffle(t1)
        np.random.shuffle(t2)

        # Shuffle order of teams
        teams = [t1, t2]
        np.random.shuffle(teams)

        # Teammates must be across from each other
        self.gs['players'].append(teams[0][0])
        self.gs['players'].append(teams[1][0])
        self.gs['players'].append(teams[0][1])
        self.gs['players'].append(teams[1][1])

        # Table order is initially just the players in order
        #   where the 0th index is for the dealer
        self.gs['table'] = self.gs['players'].copy()

        # The player left of the dealer (at 3rd index) should start the trick
        #   (be at the 0th index)
        self.gs['play_order'] = []
        self.gs['play_order'] = self.gs['players'].copy()
        new_leader = self.gs['play_order'].pop(0)
        self.gs['play_order'].append(new_leader)

    def updatePlayOrder(self, taker):
        """Updates the play order so the taker of the previous trick goes first.

        Modifies:
            self.gs['play_order']

        Args:
            taker (Player): Player that won the previous trick
        """
        while self.gs['play_order'][0] is not taker:
            new_leader = self.gs['play_order'].pop(0)
            self.gs['play_order'].append(new_leader)

    def updateTableOrder(self):
        """Selects the new dealer.

        Rotates the player order so the player to the left of the dealer
        is the new dealer.

        Modifies:
            self.gs['table']
        """
        new_dealer = self.gs['table'].pop(0)
        self.gs['table'].append(new_dealer)

    def getWinner(self):
        """Fetches the winning team.

        The team to reach 10 points first wins.

        Returns:
            (Team): Team that won, otherwise None
        """
        for team in self.gs['teams']:
            if team.points == 10:
                return team
        return None

    def logGameState(self, maker_selected=False):
        # If no log file specified, don't log
        if self.log_file is None:
            return

        # Simply log 'misdeal' if a misdeal
        if not maker_selected:
            loggable_gs = 'misdeal'
            with open(self.log_file, 'a') as f:
                json.dump(loggable_gs, f)
                f.write('\n')
            return

        team1 = [str(player) for player in self.gs['teams'][0].players]
        team2 = [str(player) for player in self.gs['teams'][1].players]

        # Re-map cards_played using strings
        cards_played = {}
        for player, cards in self.gs['cards_played'].items():
            cards_played[str(player)] = []
            for card in cards:
                cards_played[str(player)].append(str(card))

        # Convert players to strings
        trick_play_orders = []
        for players in self.gs['trick_play_orders']:
            trick_play_orders.append([str(player) for player in players])

        loggable_gs = {
            'players': [str(player) for player in self.gs['players']],
            'teams': (team1, team2),
            'table': [str(player) for player in self.gs['players']],
            'play_order': [str(player) for player in self.gs['play_order']],
            'kitty': [str(card) for card in self.gs['kitty']],
            'maker': str(self.gs['maker']),
            'trump': self.gs['trump'],
            'top_card': str(self.gs['top_card']),
            'going_alone': self.gs['going_alone'],
            'cards_played': cards_played,
            'renegers': [str(player) for player in self.gs['renegers']],
            'takers': [str(player) for player in self.gs['takers']],
            'trick_play_orders': trick_play_orders,
        }

        # Log the game
        with open(self.log_file, 'a') as f:
            json.dump(loggable_gs, f)
            f.write('\n')
