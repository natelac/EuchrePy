# EuchrePy: Python euchre game with modifiable player class

Euchre is a four player trick taking card game. This is a python implementation of euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. This project was created to develop and train AI and interface easily with a web app to display AI information and player IO.

EuchrePy also implements a euchre server that can be run on a linux computer. Up to four other players can connect to the server and play a game of euchre.

If you're unsure of how to play euchre, check out the [wikipedia page](https://en.wikipedia.org/wiki/Euchre#Rules)!

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
$ euchre-server --player-count 2
server listening for registers...
Player Alice registered
Waiting for 1 player(s)
Player Bob registered
starting game...
```

Alice's terminal:
```
$ euchre-webconsole --port 6001 --name 'Alice'

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
>>> euchre.connect(port=6002, name='Bob')

Alice, Bob have 0  AI0, AI1 have 0
--------------------------------------------------
The dealer is Bob
The top card is 9H
AI1 denied ordering up
```

For more options on the terminal commands use the ```--help``` flag. Similarily, use ```help(euchre.connect)``` for a full list of python parameters.

## Installing

From a local repository:
```
$ ls
EuchrePy
$ pip install -e EuchrePy
```

## Custom Players

You can create custom AI and use them in games as long as they are a sub-class of ```euchre.Player```. You can find its source code in ```euchre/players/player.py```

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

# Create "your" player
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

## Logging games

Games can be logged. This is a very useful feature when training AI or exploring the statistics behind euchre.

### Creating a game that logs
```python
import euchre

# Create "your" player
player = euchre.players.ConsolePlayer('User')

# Create a list of AI
ai = []
for i in range(3):
  ai.append(BasicAIPlayer('AI' + str(i)))

# Choose the teams for the game
team1 = euchre.Team(player, ai[0])
team2 = euchre.Team(ai[1], ai[2])

# Specify path to log to and play!
logged_game = euchre.StandardGame(team1, team2, log_file='euchre.log')
logged_game.play()
```

### Logging format
A game that has a misdeal simply logs "misdeal". Subsequent rounds are deliminated by newlines. The example below has the json pretty printed for readability- there are no newlines in the actual output.
```json
"misdeal"
{
    "players": ["AI2", "AI0", "AI1", "User"], 
    "teams": [
        ["User", "AI0"], 
        ["AI1", "AI2"]
    ], 
    "table": ["AI2", "AI0", "AI1", "User"], 
    "play_order": ["AI0", "AI1", "User", "AI2"], 
    "kitty": ["1C", "KS", "JC", "QH"], 
    "maker": "User", 
    "trump": "D", 
    "top_card": "KD", 
    "going_alone": false, 
    "cards_played": {
        "AI0": ["QC", "AS", "JD", "AD", "AC"], 
        "AI1": ["1H", "9S", "9C", "QS", "KC"], 
        "User": ["AH", "JS", "1D", "KD", "JH"], 
        "AI2": ["KH", "1S", "9D", "QD", "9H"]
    }, 
    "renegers": [], 
    "takers": ["User", "AI0", "AI0", "AI0", "User"], 
    "trick_play_orders": [
        ["AI2", "AI0", "AI1", "User"], 
        ["User", "AI2", "AI0", "AI1"], 
        ["AI0", "AI1", "User", "AI2"], 
        ["AI0", "AI1", "User", "AI2"], 
        ["AI0", "AI1", "User", "AI2"]
    ]
}
```

## Design decisions

The game of euchre can be coded in a lot less lines than was used in this project. However, the game would be very static and any major changes to the codebase would have knock-on effects to other parts of the code. The goal of this implementation is to be very modular and extendible.

### The Player class
The ```Player``` class's functions are called by the game.

The ```Player``` class is dynamic and can represent AI players (e.g. ```BasicAIPlayer```), human players (e.g. ```ConsolePlayer```), or even web connected players (e.g. ```WebPlayer```). Since card games are linear (each player takes one turn at a time), it is okay for the class functions to block the thread while waiting for player responses. 

The ```WebPlayer``` class uses standardized messages to communicate information to the player's client over the network. When it is called by the game it will block the games thread until it recieves a TCP message back from its client. The server creates its networking threads before it starts the game so thread blocking is okay.

### The GameServer class
The ```GameServer``` class is almost entirely game agnostic. All it does is register clients to a ```WebPlayer```, pass client responses to their ```WebPlayer```, and handle heartbeat checking.

### The StandardGame class
The ```StandardGame``` class is the least modular of the classes. Since the flow of a game is very exact, there is not alot of room for extendibility/modularity. 


## Future ideas
- [ ] Have player ports automatically picked
- [ ] Create a smart AI player
- [ ] Implement farmers hand
- [ ] Add lobby system - User can connect to server, host games, and see other games
  - This will give a purpose to ```bin/server```, continuosly host games on the server

## Known Bugs
- Only first renege should be penalized OR redo reneging logic so valid plays don't get miscounted
