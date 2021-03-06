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

from gameoflife.gameoflife import Fate

import curses
import time


class View(object):
    """A curses-based view."""

    def __init__(self, window):
        """Creates a new view."""
        self.window = window
        self.height, self.width = window.getmaxyx()

    def refresh(self, wait=False):
        """Refreshes the view curses window. If wait is True, use noutrefresh
        to delay the update, so that the screen can be updated all at once.
        """
        if wait:
            self.window.noutrefresh()
        else:
            self.window.refresh()


class CellsView(View):
    """A curses-based view of the grid of cells."""

    # These are cast to str because curses doesn't like Unicode
    MAP_FATES_CHARS = {Fate.StayDead: str(' '),
                       Fate.Birth: str(' '),
                       Fate.Survive: str('o'),
                       Fate.DeathByIsolation: str('*'),
                       Fate.DeathByOvercrowding: str('O')}

    def ink(self, age):
        """Returns the color to use according to how old the cell is."""
        if age == 0:
            ink = curses.color_pair(3) | curses.A_BOLD
        elif age == 1:
            ink = curses.color_pair(4) | curses.A_BOLD
        elif age < 5:
            ink = curses.color_pair(6) | curses.A_BOLD
        else:
            ink = curses.color_pair(1) | curses.A_BOLD
        return ink

    def draw(self, game, pos_x, pos_y, color):
        """Draws the cells."""
        for row in range(self.height):
            for col in range(self.width):
                # Choose char according to fate
                fate = game.fate(row + pos_y, col + pos_x)
                char = self.MAP_FATES_CHARS[fate]

                # Choose ink according to age
                if color:
                    age = game.age(row + pos_y, col + pos_x)
                    ink = self.ink(age)
                else:
                    ink = 0

                # Draw the cell
                try:
                    self.window.addch(row, col, char, ink)
                except curses.error:
                    # After drawing the last character, the cursor moves out
                    # of the window, causing curses to raise an error.
                    # Just ignore it.
                    pass


class GameView(View):
    """A curses-based view of the whole game."""

    def draw(self, app, game):
        """Draws the current state of the game."""

        # Window border
        self.window.border()

        # Position
        self.window.addstr(0, 2, ' X = {} - Y = {} '.format(app.pos_x,
                                                            app.pos_y))

        # Clock
        self.window.addstr(0, self.width - 12, time.strftime(' %H:%M:%S '))

        # Generation number
        self.window.addstr(self.height - 1, 2,
                           ' Generation: {} '.format(game.generation))

        # Speed factor
        speed_str = '{:2.1f}x'.format(app.speed) if not app.paused else '---'
        self.window.addstr(self.height - 1, self.width - 15,
                           ' Speed: {} '.format(speed_str))
