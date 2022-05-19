# EuchrePy: Euchre Game With Modifiable Player Interface

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. EuchrePy was created to train AI and interface easily with a web app to display AI information and player IO.

Furthermore, this is meant to be able to run as an instance of a euchre game running on a flask server between 4 players.

The goal of the 'rework' branch is to simplify the game logic, and simplify how information is passed between objects.

[Monte Carlo Tree Search (MCTS)](https://github.com/matgrioni/Euchre-bot) and [Neural Fictitious Self-Play (NFSP)](https://arxiv.org/pdf/1603.01121.pdf) have been used to different levels of success to create AI for imperfect-information games (Euchre and Poker respectively). I am looking to use Monte Carlo Neural Fictitious Self-Play (MC-NFSP) to create an AI for playing Euchre. My goal is to implement the methods used for poker described by [Zhang et. al](https://arxiv.org/pdf/1903.09569.pdf) to create an MC-NFSP Euchre AI.

(Maybe I'll implement MCTS, then NFSP, then MC-NFSP)

*NSFP was [already implemented](https://github.com/elipugh/euchre) in Euchre. The paper for NFSP and Q-learning in Euchre is actually a student paper. I think for MCTS you should link to an actual paper, not a bot by a single person. The MCTS and NFSP papers do not explicitly discuss feature selection. I think I could get better performance by creating better features. There was [another paper](https://sites.ualberta.ca/~amw8/hearts.pdf) that talked about what features to select for a game of hearts, which might be a good reference.*

## Install
- Run 'sudo pip install -e .'

## TODO:
### Now
- Come up with better terminology rather than "update" for webplayer
- Get webconsole.py to register with server and print connection complete
- Get a loop in webconsole.py for waiting for commands from server and prompting the user
- Implement consolewebplayer.py so server can send commands to webconsole.py
- Have functions to call, rather than dictionaries passed to Players
  - For example: msgPoints, rather than passing a dictionary to passMsg

- Networking questions:
  - What if player doesn't respond to request? When to resend/how to resend?

### Short Term
- On player disconnect, save game

### Bugs
- Fix bug where if you renege, AI0 reneges with
  ERROR:
  You reneged by playing 9H and the opposing team was awarded 2 points
  AI0 reneged by playing AI0 and your team was awarded 2 points
- Fix bug where if going alone, your partner will start the trick (which shouldn't be able to happen) and the continue doesn't work?

### Short Term
- Euchre() class as a driver instead
- Check for whether a player played cards only from their hand.
- Simple intelligent plays for BasicAI rather than just random valid plays.

## Ideas
- Work on user experience, IE "import EuchrePy as euch"
  - "euch.playGame()"
    - Defaults to a console game against AI
- Add game save states in the event of crashes
- Add WebPlayer that is a separate thread that sends messages to a client
- Game Class that can be extended to create variations of euchre
  - Refactor code so StandardGame extends Game
- MLPlayer that makes decisions from a trained ML/ interfaces with one
to train it? Along with a driver class that will train the network by
running through the game?
- Switch to poetry from setup tools
