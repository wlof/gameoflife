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

"""This module provides the class for the main game application.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import curses
import time

from gameoflife.ui.views import GameView, CellsView


class GameApp(object):
    """Main game application.

    Manages the view and handles user input.
    """

    MIN_SPEED = 0.1   # minimum game speed factor
    MAX_SPEED = 16.0  # maximum game speed factor

    SCREEN_DRAW_FREQ = 30.0  # frequency at which the screen is redrawn

    def __init__(self, game, stdscr):
        """Creates a new game application."""

        self.game = game
        self.screen = stdscr

        self.paused = False
        self.quit = False
        self.speed = 1.0
        self.pos_x, self.pos_y = 0, 0

        self._last_gen_time = time.time()
        self._last_draw_time = time.time()

        self.init_views()

    def init_views(self):
        """Initializes the game and cells views."""

        # Create the game view
        self.game_view = GameView(self.screen)

        # The cells view dimensions are the main view dimensions minus 2, to
        # leave room for the border
        height, width = self.screen.getmaxyx()
        cells_view_height, cells_view_width = height - 2, width - 2
        cells_view_window = self.screen.derwin(cells_view_height,
                                               cells_view_width,
                                               1, 1)

        # Create the cells view
        self.cells_view = CellsView(cells_view_window)

    def main(self):
        """Event loop."""

        # Set non-blocking mode for keyboard events
        self.screen.nodelay(1)
        self.screen.timeout(0)

        # Initialize internal clock
        self._prev_clock = time.time()

        # First draw
        self.draw()

        while not self.quit:
            # Get key press, and pass it to handler.
            char = self.screen.getch()
            if char != -1:
                self.handle_keypress(char)

            # Get current time
            clock = time.time()

            # Is it time for a new generation?
            if clock - self._last_gen_time > 1.0 / self.speed:
                if not self.paused:
                    self.game.next_generation()
                    self._last_gen_time = clock

            # Is it time to redraw the screen?
            if clock - self._last_draw_time > 1.0 / GameApp.SCREEN_DRAW_FREQ:
                self.draw()
                self._last_draw_time = clock

            # Sleep a bit before next iteration
            time.sleep(0)

    def handle_keypress(self, char):
        """Key press handler."""

        # TODO: rewrite this in a less ugly manner. Perhaps a handler
        #       decorator?

        if char == curses.KEY_RESIZE:
            # Terminal was resized: reinitialize the views
            self.init_views()

        elif char in (ord("q"), 27):
            # Q or Escape: end
            self.quit = True

        elif char == ord("r"):
            # Q or Escape: end
            self.game.reset()

        elif char == ord(" "):
            # Space bar: pause / unpause
            self.paused = not self.paused

        elif char == ord("\n") or char == curses.KEY_ENTER:
            # Enter: advance turn, but only when paused
            if self.paused:
                self.game.next_generation()

        elif char in (ord("+"), 465):
            # +: increase speed
            self.increase_speed()

        elif char in (ord("-"), 464):
            # -: decrease speed
            self.decrease_speed()

        elif char == curses.KEY_LEFT:
            self.pos_x = (self.pos_x - 1) % self.game.width

        elif char == curses.KEY_RIGHT:
            self.pos_x = (self.pos_x + 1) % self.game.width

        elif char == curses.KEY_UP:
            self.pos_y = (self.pos_y - 1) % self.game.height

        elif char == curses.KEY_DOWN:
            self.pos_y = (self.pos_y + 1) % self.game.height

    def draw(self):
        """Draws the current state of the game."""

        # Draw main window (border, speed, etc.)
        self.game_view.draw(self, self.game)
        self.game_view.refresh(wait=True)

        # Draw the view of the cells
        self.cells_view.draw(self.game, self.pos_x, self.pos_y)
        self.cells_view.refresh(wait=True)

        # Actually redraw the screen
        curses.doupdate()

    def increase_speed(self):
        """Increases game speed (if not paused)."""
        if not self.paused:
            self.speed *= 2.0
            if self.speed > GameApp.MAX_SPEED:
                self.speed = GameApp.MAX_SPEED

    def decrease_speed(self):
        """Decreases game speed (if not paused)."""
        if not self.paused:
            self.speed /= 2.0
            if self.speed < GameApp.MIN_SPEED:
                self.speed = GameApp.MIN_SPEED
