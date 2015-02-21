#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import random
import sys
import threading
import time


class CircularList(list):
    """
    Circular list class.

    Permits accessing elements by out-of-range indexing, i.e. indexes are
    modulo'd by the list's length.

    Does not (yet?) support out-of-range splicing.
    """

    def __getitem__(self, key):
        return list.__getitem__(self, key % len(self))

    def __setitem__(self, key, value):
        list.__setitem__(self, key % len(self), value)


class TorusGrid(object):
    """
    A grid whose edges are connected.

    Basically, a circular 2D array. Dimensions are set at construction time.
    """

    def __init__(self, width, height, init_value=0):
        """
        Constructor.
        """
        self.width = width
        self.height = height
        self._rows = [CircularList([init_value] * width)
                      for _ in range(height)]

    def __getitem__(self, idx):
        return self._rows[idx % len(self._rows)]

    def __setitem__(self, idx, value):
        self._rows[idx % len(self._rows)] = value

    def __str__(self):
        s = "\n".join([" ".join([str(item) for item in row])
                       for row in self._rows])
        return s + "\n"


class CellGrid(TorusGrid):
    """
    Grid of cells.

    Each position in the grid can have one of two values:
    - True if there is a live cell at this location
    - False if there isn't
    """

    def __init__(self, width, height):
        """
        Constructor.
        """
        super(CellGrid, self).__init__(width, height, False)

    def __str__(self):
        s = "\n".join([" ".join(["#" if item is True else " " for item in row])
                       for row in self._rows])
        return s + "\n"

    def populate_random(self, prob=0.1):
        """
        Populates the grid at random, with specified probability.
        """
        for row in range(self.height):
            for col in range(self.width):
                self[row][col] = True if random.random() < prob else False

    def get_number_neighbours(self, row, col):
        """
        Returns the number of cells in the Moore neighbourhood of the
        specified location.
        """

        # Could probably rewrite this more pythonically with a list
        # comprehension, but needs splice support in CircularList first.
        number_neighours = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i, j) == (row, col):
                    # Don't count the location itself
                    continue
                if self[i][j]:
                    number_neighours += 1
        return number_neighours

    def apply_states(self, states):
        """
        Kills and spawns cells according to the grid of states.
        """
        for row in range(self.height):
            for col in range(self.width):
                if states[row][col] in (States.DeathByIsolation,
                                        States.DeathByOverpopulation):
                    self[row][col] = False
                elif states[row][col] == States.Birth:
                    self[row][col] = True


class States:
    """
    Enumerate of the possible states.
    """

    NoChange, Birth, DeathByIsolation, DeathByOverpopulation = range(4)


class StateGrid(TorusGrid):
    """
    Grid of states.
    """

    N_B = 3      # Number of neighbours needed for a cell to be born
    N_S_MIN = 2  # Minimum number of neighbours needed for a cell to stay alive
    N_S_MAX = 3  # Maximum number of neighbours needed for a cell to stay alive

    def __init__(self, width, height):
        """
        Constructor.
        """
        super(StateGrid, self).__init__(width, height, States.NoChange)

    def __str__(self):
        s = "\n".join(["".join([str(item) for item in row])
                       for row in self._rows])
        return s + "\n"

    def compute(self, cells):
        """
        Compute states according to the grid of cells.
        """
        for row in range(self.height):
            for col in range(self.width):
                number_neighours = cells.get_number_neighbours(row, col)

                if cells[row][col] is True:
                    if number_neighours < StateGrid.N_S_MIN:
                        self[row][col] = States.DeathByIsolation
                    elif number_neighours > StateGrid.N_S_MAX:
                        self[row][col] = States.DeathByOverpopulation
                    else:
                        self[row][col] = States.NoChange
                else:
                    if number_neighours == StateGrid.N_B:
                        self[row][col] = States.Birth
                    else:
                        self[row][col] = States.NoChange


class ResizeException(Exception):
    """
    Exception class to handle (or rather, not handle) resize events.

    Doesn't do anything useful. Or at all.
    """

    pass


class Game(object):
    """
    Main class.

    This class handles most of the non-math aspects of the game: drawing the
    screen, handling key presses, passing time, etc.
    """

    CHAR_CELL_LIVE = "*"  # character used to draw live cells
    CHAR_CELL_DEAD = " "  # character used to draw dead cells

    MIN_SPEED = 0.1   # minimum game speed factor
    MAX_SPEED = 32.0  # maximum game speed factor

    def __init__(self, screen):
        """
        Constructor.
        """

        self.screen = screen
        self.screen.nodelay(0)

        # Get terminal size
        self.height, self.width = self.screen.getmaxyx()

        # Initialize attributes
        self.generation = 1
        self.speed = 1.0
        self.paused = False
        self.quit = False

        # World size is terminal size minus two, to leave room for the screen
        # border.
        self.world_width = self.width - 2
        self.world_height = self.height - 2
        self.world_window = self.screen.derwin(self.world_height,
                                               self.world_width,
                                               1, 1)

        # Instantiate cell grid and populates it at random
        self.cells = CellGrid(self.world_width, self.world_height)
        self.cells.populate_random()

        # Instantiate state grid
        self.states = StateGrid(self.world_width, self.world_height)

        # Instantiate threads
        self.thread_draw = threading.Thread(target=self._thread_draw)
        self.thread_draw.daemon = True
        self.thread_time = threading.Thread(target=self._thread_time)
        self.thread_time.daemon = True

    def main(self):
        """
        Event loop.

        Also starts the threads.
        """

        # Let's start drawing ASAP.
        self.thread_draw.start()

        # Let the first generation enjoy a full second of glorious
        # immortality before starting time.
        time.sleep(1.0)
        self.thread_time.start()

        while not self.quit:
            # Get key press, and pass it to handler.
            char = self.screen.getch()
            self.handle_keypress(char)

    def reset(self):
        """
        Resets the game.
        """

        # Saves pause state and use paused flag as a poor man's mutex.
        pause_state = self.paused
        self.paused = True

        # Resets grids
        self.cells = CellGrid(self.world_width, self.world_height)
        self.cells.populate_random()
        self.states = StateGrid(self.world_width, self.world_height)
        self.generation = 1

        # Restore pause state
        self.paused = pause_state

    def increase_speed(self):
        """
        Increases game speed (if not paused).
        """
        if not self.paused:
            self.speed *= 2.0
            if self.speed > Game.MAX_SPEED:
                self.speed = Game.MAX_SPEED

    def decrease_speed(self):
        """
        Decreases game speed (if not paused).
        """
        if not self.paused:
            self.speed /= 2.0
            if self.speed < Game.MIN_SPEED:
                self.speed = Game.MIN_SPEED

    def handle_keypress(self, char):
        """
        Handles key presses.
        """

        if char == curses.KEY_RESIZE:
            # Should probably handle this more gracefully, but in the
            # meantime...
            raise ResizeException

        elif char == ord("q") or char == 27:
            # Q or Escape: end
            self.quit = True

        elif char == ord("r"):
            # Q or Escape: end
            self.reset()

        elif char == ord(" "):
            # Space bar: pause / unpause
            self.paused = not self.paused

        elif char == ord("\n") or char == curses.KEY_ENTER:
            # Enter: advance turn, but only when paused
            if self.paused:
                self.next_generation()

        elif char == ord("+"):
            # +: increase speed
            self.increase_speed()

        elif char == ord("-"):
            # -: decrease speed
            self.decrease_speed()

    def next_generation(self):
        """
        Triggers the next generation of cells.
        """
        self.states.compute(self.cells)
        self.cells.apply_states(self.states)
        self.generation += 1

    def draw(self):
        """
        Draws ALL THE THINGS (cells & main window).
        """
        self.draw_world()
        self.draw_screen()

    def draw_screen(self):
        """
        Draws the main window: border, title, clock, and "status bar".
        """

        # Window border
        self.screen.border()

        # Title
        self.screen.addstr(0, 10, " GAME OF LIFE ")

        # Clock
        self.screen.addstr(0, self.width - 12, time.strftime(" %H:%M:%S "))

        # Generation number
        self.screen.addstr(self.height - 1, 2,
                           " Generation: {} ".format(self.generation))

        # Speed factor
        speed_str = "{:2.1f}x".format(self.speed) if not self.paused else "---"
        self.screen.addstr(self.height - 1, self.width - 15,
                           " Speed: {} ".format(speed_str))

        self.screen.refresh()

    def draw_world(self):
        """
        Draws the world, i.e. the grid of cells.
        """
        for row in range(self.world_height):
            for col in range(self.world_width):
                if self.cells[row][col] is True:
                    char = Game.CHAR_CELL_LIVE
                else:
                    char = Game.CHAR_CELL_DEAD

                # Cells born this generation are drawn in a different colour
                if self.states[row][col] == States.Birth:
                    ink = curses.color_pair(1)
                else:
                    ink = curses.color_pair(0)

                try:
                    self.world_window.addch(row, col, char, ink)
                except curses.error:
                    # After drawing the last character, the cursor moves out
                    # of the window, causing curses to raise an error.
                    # Just ignore it.
                    pass

        self.world_window.refresh()

    def _thread_draw(self):
        """
        Drawing thread function.

        Refreshes the screen at ~20 Hz.
        """
        while True:
            self.draw()
            time.sleep(0.05)

    def _thread_time(self):
        """
        Passage of time thread function.

        Triggers the computing of next generations according to the speed
        factor (when game is not paused).
        """
        while True:
            if not self.paused:
                self.next_generation()
                sleep_time = 1.0 / self.speed
            else:
                sleep_time = 0.02

            time.sleep(sleep_time)


def main_wrapped(stdscr):
    """
    Actual main function.

    This is called by the curses wrapper, with the main screen object as a
    parameter.
    """

    # Initialize the colour pairs used by the game.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Setup curses
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.refresh()

    # Instantiate the game class and start the event loop.
    game = Game(stdscr)
    game.main()


def main():
    """
    Main function.
    """

    try:
        curses.wrapper(main_wrapped)
    except ResizeException:
        print("Please do not resize the terminal while game is running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
