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

from gameoflife.ui.views import GameView
from gameoflife.ui.exceptions import ResizeException


class GameApp(object):
    """Main game application.

    Manages the view and handles user input.
    """

    MIN_SPEED = 0.1   # minimum game speed factor
    MAX_SPEED = 16.0  # maximum game speed factor

    def __init__(self, game, stdscr):
        """Creates a new game application."""

        self.game = game
        self.screen = stdscr

        self.paused = False
        self.quit = False
        self.speed = 1.0

        self._prev_clock = time.time()

        self.view = GameView(self.screen)

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

            # Draw the screen
            self.draw()

            # Is it time for a new generation?
            clock = time.time()
            if clock - self._prev_clock > 1.0 / self.speed:
                if not self.paused:
                    self.game.next_generation()
                self._prev_clock = clock

            # Sleep a bit before next iteration
            time.sleep(0.01)

    def handle_keypress(self, char):
        """Key press handler."""

        if char == curses.KEY_RESIZE:
            # Should probably handle this more gracefully, but in the
            # meantime...
            raise ResizeException

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

        elif char == ord("+"):
            # +: increase speed
            self.increase_speed()

        elif char == ord("-"):
            # -: decrease speed
            self.decrease_speed()

    def draw(self):
        """Draw the current state of the game."""
        self.view.draw(self, self.game)

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
