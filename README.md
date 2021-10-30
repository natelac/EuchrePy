# EuchrePy: Euchre Game With Modifiable Player Interface

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. EuchrePy was created to train AI and interface easily with a web app to display AI information and player IO.

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
