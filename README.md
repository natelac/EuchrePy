# EuchrePy: Euchre game with modifiable player interface

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. EuchrePy was created to train AI and interface easily with a web app to display AI information and player IO.

Furthermore, this is meant to be able to run as an instance of a euchre game running on a flask server between 4 players.

The goal of the 'rework' branch is to simplify the game logic, and simplify how information is passed between objects.

[Monte Carlo Tree Search (MCTS)](https://github.com/matgrioni/Euchre-bot) and [Neural Fictitious Self-Play (NFSP)](https://arxiv.org/pdf/1603.01121.pdf) have been used to different levels of success to create AI for imperfect-information games (Euchre and Poker respectively). I am looking to use Monte Carlo Neural Fictitious Self-Play (MC-NFSP) to create an AI for playing Euchre. My goal is to implement the methods used for poker described by [Zhang et. al](https://arxiv.org/pdf/1903.09569.pdf) to create an MC-NFSP Euchre AI.

(Maybe I'll implement MCTS, then NFSP, then MC-NFSP)

*NSFP was [already implemented](https://github.com/elipugh/euchre) in Euchre. The paper for NFSP and Q-learning in Euchre is actually a student paper. I think for MCTS you should link to an actual paper, not a bot by a single person. The MCTS and NFSP papers do not explicitly discuss feature selection. I think I could get better performance by creating better features. There was [another paper](https://sites.ualberta.ca/~amw8/hearts.pdf) that talked about what features to select for a game of hearts, which might be a good reference.*


## Install
- Run 'sudo pip install -e .'

## Features
- [x] Complete game state object that can be exported at end of play
- [ ] Add heartbeat checking
- [ ] Create a smartAI Player
- [ ] Run PEP8 on all of the code
- [ ] Start using semantic versioning describe in this [stackoverflow post](https://stackoverflow.com/questions/37814286/how-to-manage-the-version-number-in-git), and release "v0.1.0" !

## Known Bugs
- Only first renege should be penalized OR redo reneging logic so valid plays don't get miscounted

## Future ideas
- Implement farmers hand
- Add lobby system - User can connect to server, host games, and see other games

## Other projects
- AI project
  - Move all AI stuff to a separate project
  - Explore coding different strategies and having them compete against each other
  - Train AI using self play
