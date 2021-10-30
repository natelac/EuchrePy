# EuchrePy: Euchre Game With Modifiable Player Interface

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. EuchrePy was created to train AI and interface easily with a web app to display AI information and player IO.

[Monte Carlo Tree Search (MCTS)](https://github.com/matgrioni/Euchre-bot) and [Neural Fictitious Self-Play (NFSP)](https://arxiv.org/pdf/1603.01121.pdf) have been used to different levels of success to create AI for imperfect-information games (Euchre and Poker respectively). I am looking to use Monte Carlo Neural Fictitious Self-Play (MC-NFSP) to create an AI for playing Euchre. My goal is to implement the methods used for poker described by [Zhang et. al](https://arxiv.org/pdf/1903.09569.pdf) to create my MC-NFSP Euchre AI.

## TODO:

### Short Term
- Remove unnecessary functions from every class.
- Finish up scoring for whoever takes majority tricks
  - Possibly finish up scoring for everything
- First to 10 declared getWinner
- Going Alone
- Clean up code,
- organize methods,
- create doc strings
- Make Euchre() class as driver instead

### Long Term
- APIPlayer for interfacing with a webapp through javascript
- Create a Game Class that can be extended to create variations of euchre
- MLPlayer that makes decisions from a trained ML/ interfaces with one
to train it? Along with a driver class that will train the network by
running through the game?
