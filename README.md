# EuchrePy: Euchre Game With Modifiable Player Interface

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. EuchrePy was created to train AI and interface easily with a web app to display AI information and player IO.

[Monte Carlo Tree Search (MCTS)](https://github.com/matgrioni/Euchre-bot) and [Neural Fictitious Self-Play (NFSP)](https://arxiv.org/pdf/1603.01121.pdf) have been used to different levels of success to create AI for imperfect-information games (Euchre and Poker respectively). I am looking to use Monte Carlo Neural Fictitious Self-Play (MC-NFSP) to create an AI for playing Euchre. My goal is to implement the methods used for poker described by [Zhang et. al](https://arxiv.org/pdf/1903.09569.pdf) to create an MC-NFSP Euchre AI.

(Maybe I'll implement MCTS, then NFSP, then MC-NFSP)

*NSFP was [already implemented](https://github.com/elipugh/euchre) in Euchre. The paper for NFSP and Q-learning in Euchre is actually a student paper. I think for MCTS you should link to an actual paper, not a bot by a single person. The MCTS and NFSP papers do not explicitly discuss feature selection. I think I could get better performance by creating better features. There was [another paper](https://sites.ualberta.ca/~amw8/hearts.pdf) that talked about what features to select for a game of hearts, which might be a good reference.*

## TODO:
- Scoring
- Going alone
  - If a player is going alone, just skip over their partner. You might also need to update the code for checking reneges
- Simple intelligent plays for BasicAI rather than just random valid plays.

### Short Term
- Make a Euchre() class as a driver instead
  - Let's you select what type of game to play, easy control of
- Add checking for whether a player played cards only from their hand.

### Long Term
- JSPlayer for interfacing with a webapp through javascript
- Game Class that can be extended to create variations of euchre
  - Refactor code so StandardGame extends Game
- MLPlayer that makes decisions from a trained ML/ interfaces with one
to train it? Along with a driver class that will train the network by
running through the game?
