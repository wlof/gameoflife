## Game of Life

This is a simple Python module implementing [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), with a curses-based UI.

The game runs on a torus (i.e. the edges of the screen are connected). Default size is 100x100.

![Game of Life](https://i.imgur.com/umMh1lu.gif)

### Installation
From GitHub:
```
$ git clone https://github.com/wlof/gameoflife
$ cd gameoflife
$ sudo python setup.py install
```

If you're running Windows, you will need to install the unofficial curses library. Download it from http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses.

If you want to use the slightly faster NumPy/SciPy implementations, you will of course have to install these libraries: http://www.scipy.org/scipylib/download.html

### Usage
After installation, run the game using:
```
gameoflife
```

There a few arguments you can use:
```
usage: gameoflife [--impl {normal,light,numpy,numpy-light}] [--width WIDTH]
                  [--height HEIGHT] [--prob PROB] [--color {auto,yes,no}]
                  [--version] [--help]

Conway's Game of Life

optional arguments:
  --impl {normal,light,numpy,numpy-light}, -i {normal,light,numpy,numpy-light}
                        game implementation
  --width WIDTH, -w WIDTH
                        grid width
  --height HEIGHT, -h HEIGHT
                        grid height
  --prob PROB, -p PROB  initial population probability
  --color {auto,yes,no}, -c {auto,yes,no}
                        use colors
  --version             show program's version number and exit
  --help                show this help message and exit

Suggestions and bug reports are greatly appreciated:
https://github.com/wlof/gameoflife/issues
```

### Implementations

There are four different implementations that you can use (with the `--impl` command line argument):
- normal: this is the basic implementation. It has all features and requires no external libraries, but isn't too fast.
- light: does not keep track of the fates and ages of the cells. As a result, it is faster than the normal implementation.
- numpy: NumPy/SciPy-based full-featured implementation
- numpy-light: NumPy/SciPy-based light implementation

### Legend

The cells are represented as follows:
- `*`: the cell will die of isolation in the next generation
- `o`: the cell will survive in the next generation
- `O`: the cell will die of overcrowding in the next generation

Additionally, the color of each cell indicates its age:
- yellow: the cell was just born this generation
- green: the cell was born one generation ago
- cyan: the cell was born between 2 and 4 generations ago
- white: the cell was born 5 or more generations ago

### Manual
During the game, you may use the following keys:
- arrow keys: move around
- Escape or Q: quit the game
- Space: pause / unpause
- Enter: when game is paused, advance turn manually
- + and -: increase / decrease game speed
- R: reset the game (repopulates at random)
