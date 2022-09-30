# EuchrePy: Euchre game with modifiable player class

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. This project was created to develop and train AI and interface easily with a web app to display AI information and player IO.

Also implements a euchre server that can be run on a linux computer. Up to four other players can connect to the server and play a game of euchre.

## Example

### Playing a local game
In a python interactive shell:
```python
>>> import euchre
>>> euchre.play()

User, AI0 have 0 points  AI1, AI2 have 0 points
--------------------------------------------------
The dealer is AI2
The top card is [ QC ]
AI0 denied ordering up
AI1 denied ordering up
Cards: [ AC ], [ 9S ], [ 1C ], [ KS ], [ QD ]
Order up? y/n
```

From the terminal:
```
$ euchre-play

User, AI0 have 0 points  AI1, AI2 have 0 points
--------------------------------------------------
The dealer is AI2
...
```

### Hosting and playing an online game
Server terminal:
```
$ euchre-server --host localhost --port 6000 --hb-port 5999 --player-count 2
server listening for registers...
Player Alice registered
Waiting for 1 player(s)
Player Bob registered
starting game...
```

Alice's terminal:
```
$ euchre-console --port 6001 --server-port 6000 --name 'Alice'

Alice, Bob have 0  AI0, AI1 have 0
--------------------------------------------------
The dealer is Bob
The top card is 9H
AI1 denied ordering up
Cards: [ KC ], [ JS ], [ 1H ], [ 9S ], [ JC ]
Order up? y/n
```

Bob's interactive python shell:
```python
>>> import euchre
>>> euchre.connect(port=6002, server_port=6000, name='Bob')

Alice, Bob have 0  AI0, AI1 have 0
--------------------------------------------------
The dealer is Bob
The top card is 9H
AI1 denied ordering up
```

## Installing

From local repository:
```
$ ls
EuchrePy
$ pip install -e EuchrePy
```

## Custom Players

You can create custom AI and use them in games as long as they are a sub-class of ```euchre.Player```.

### Creating a custom Player class

For a list of helper functions and abstract methods to implement, use ```help(euchre.Player)```

```python
# customplayer.py

import abc
import euchre

class CustomPlayer(euchre.Player, abc.ABC):
  pass
  
# The code below will error, giving you a list of abstract methods you need to implement
player = CustomPlayer()
```
### Playing a game with custom Players

```python
import euchre
from customplayer import CustomPlayer

player = euchre.players.ConsolePlayer('User')

# Create a list of your custom AI
ai = []
for i in range(3):
  ai.append(CustomPlayer('AI' + str(i)))

# Choose the teams for the game
team1 = euchre.Team(player, ai[0])
team2 = euchre.Team(ai[1], ai[2])

# Start the game!
game = euchre.StandardGame(team1, team2)
game.play()
```

## Future ideas
- [ ] Create a smart AI player
- [ ] Implement farmers hand
- [ ] Add lobby system - User can connect to server, host games, and see other games
  - This will give a purpose to ```bin/server```, continuosly host games on the server

## Known Bugs
- Only first renege should be penalized OR redo reneging logic so valid plays don't get miscounted
