## Game of Life

This is a simple Python script implementing [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using the curses library.

The game runs on a torus (i.e. the edges of the screen are connected). Default size is 100x100.

### Installation
Download the project files and install using:
```
python setup.py install
```

If you want to use the slightly faster NumPy/SciPy implementation, you will of course have to install these libraries: http://www.scipy.org/scipylib/download.html

If you're running Windows, you will have to install the unofficial curses library first. Download it from http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses.

### Usage
After installation, run the game using:
```
gameoflife
```

There a few arguments you can use:
```
usage: gameoflife [--numpy] [--width WIDTH] [--height HEIGHT] [--version]
                  [--help]

Conway's Game of Life

optional arguments:
  --numpy, -n           use the NumPy implementation
  --width WIDTH, -w WIDTH
                        grid width
  --height HEIGHT, -h HEIGHT
                        grid height
  --version             show program's version number and exit
  --help                show this help message and exit

Suggestions and bug reports are greatly appreciated:
https://github.com/wlof/gameoflife/issues
```

### Manual
During the game, you may use the following keys:
- arrow keys: move around
- Escape or Q: quit the game
- Space: pause / unpause
- Enter: when game is paused, advance turn manually
- + and -: increase / decrease game speed
- R: reset the game (repopulates at random)
