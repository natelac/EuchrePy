# EuchrePy: Euchre game with modifiable player class

An implementation of Euchre designed to be easily extendible. The player input-output (IO) is separated from the game logic by a Player class. This project was created to develop and train AI and interface easily with a web app to display AI information and player IO.

Also implements a euchre server that can be run on a linux computer. Up to four other players can connect to the server and play a game of euchre.

## Example

### Playing a local game
In a python3 interactive shell:
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

Alice's terminal
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

Bob's terminal
```
$ euchre-webconsole --port 6002 --server-port 6000 --name 'Bob'
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

## Making your own Player class

## Future ideas
- [ ] Create a smart AI player
- [ ] Implement farmers hand
- [ ] Add lobby system - User can connect to server, host games, and see other games

## Known Bugs
- Only first renege should be penalized OR redo reneging logic so valid plays don't get miscounted
