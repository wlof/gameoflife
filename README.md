## Game of Life

This is a simple Python script implementing [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using the curses library.

The game runs on a torus (the edges of the screen are connected). Size is set by the terminal.

### Usage
Just run gameoflife.py. It should be compatible with both Python 2 and 3, and requires no additional libraries.

Except if you're running Windows, in which case you will have to install the unofficial curses library first. Download it from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses).

### Manual
During the game, you may use the following keys:
- Escape or Q: quit the game
- Space: pause / unpause
- Enter: when game is paused, advance turn manually
- + and -: increase / decrease game speed
- R: reset the game (repopulates at random)