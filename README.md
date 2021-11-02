# EuchrePy: Euchre Game With Modifiable Player Interface

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. EuchrePy was created to train AI and interface easily with a web app to display AI information and player IO.

[Monte Carlo Tree Search (MCTS)](https://github.com/matgrioni/Euchre-bot) and [Neural Fictitious Self-Play (NFSP)](https://arxiv.org/pdf/1603.01121.pdf) have been used to different levels of success to create AI for imperfect-information games (Euchre and Poker respectively). I am looking to use Monte Carlo Neural Fictitious Self-Play (MC-NFSP) to create an AI for playing Euchre. My goal is to implement the methods used for poker described by [Zhang et. al](https://arxiv.org/pdf/1903.09569.pdf) to create an MC-NFSP Euchre AI.

(Maybe I'll implement MCTS, then NFSP, then MC-NFSP)

*NSFP was implemented https://github.com/elipugh/euchre. The paper for NFSP and Q-learning in Euchre is actually a student paper. I think for MCTS you should link to an actual paper, not a bot by a single person. I think either the NFSP or MCTS didn't explicitly have feature selection, and I think they trained it on the raw features. I think I could get better performance by creating better features. There was another paper that talked about what features to select, so I think that would be a good reference. I forget which paper it is (I don't think it was explicitly euchre, maybe just poker.*

## TODO:

### Short Term
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
