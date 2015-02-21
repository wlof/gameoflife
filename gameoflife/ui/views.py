# -*- coding: utf-8 -*-

# This file is part of gameoflife.
# Copyright 2015, wlof.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""This module provides the default commands for beets' command-line
interface.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import curses
import time

from gameoflife.grids import States


class View(object):
    """A curses-based view."""

    def __init__(self, window):
        """Creates a new view."""
        self.window = window
        self.height, self.width = window.getmaxyx()


class CellsView(View):
    """A curses-based view of the grid of cells."""

    CHAR_CELL_LIVE = '*'  # character used to draw live cells
    CHAR_CELL_DEAD = ' '  # character used to draw dead cells

    def draw(self, game):
        """Draws the cells."""
        for row in range(self.height):
            for col in range(self.width):
                # Pick the character according to the cell state (alive or
                # dead)
                if game.cells[row][col] is True:
                    char = str(CellsView.CHAR_CELL_LIVE)
                else:
                    char = str(CellsView.CHAR_CELL_DEAD)

                # Cells born this generation are drawn in a different colour
                if game.states[row][col] == States.Birth:
                    ink = curses.color_pair(1)
                else:
                    ink = curses.color_pair(0)

                # Draw the cell
                try:
                    self.window.addch(row, col, char, ink)
                except curses.error:
                    # After drawing the last character, the cursor moves out
                    # of the window, causing curses to raise an error.
                    # Just ignore it.
                    pass

        self.window.refresh()


class GameView(View):
    """A curses-based view of the whole game."""

    def __init__(self, window):
        """Creates a new view."""
        super(GameView, self).__init__(window)
        self.init_cells_view()

    def init_cells_view(self):
        """Initializes the cells subview."""
        # The cells view dimensions are the main view dimensions minus 2, to
        # leave room for the border
        cells_view_height, cells_view_width = self.height - 2, self.width - 2
        cells_view_window = self.window.derwin(cells_view_height,
                                               cells_view_width,
                                               1, 1)

        # Create the cells view
        self.cells_view = CellsView(cells_view_window)

    def draw(self, app, game):
        """Draws the current state of the game."""

        # Window border
        self.window.border()

        # Title
        self.window.addstr(0, 10, " GAME OF LIFE ")

        # Clock
        self.window.addstr(0, self.width - 12, time.strftime(" %H:%M:%S "))

        # Generation number
        self.window.addstr(self.height - 1, 2,
                           " Generation: {} ".format(game.generation))

        # Speed factor
        speed_str = "{:2.1f}x".format(app.speed) if not app.paused else "---"
        self.window.addstr(self.height - 1, self.width - 15,
                           " Speed: {} ".format(speed_str))

        # Draw the cells
        self.cells_view.draw(game)

        self.window.refresh()
