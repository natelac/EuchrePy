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
- Have new_trump message being sent, hnd having trump displayed for webconsole in spots it was commented out
- Finish webconsole
- Implement picking card to swap

### Short Term
- Create a public game info dict structure that stores the local information for webconsole, and which can be used in React
  - This might make more sense in context of a 'javscriptplayer' class
- Have information about who is currently ordering up be sent to all payers
- Setup threading when sending informational messages
  - Make sure that players recieve information in order
- Networking questions:
  - What if player doesn't respond to request? When to resend/how to resend?
    - Currently it goes endlessly, but for sending regular messages it might throw an error
- On player disconnect, save game
### Bugs
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
