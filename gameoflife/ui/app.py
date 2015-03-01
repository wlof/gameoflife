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


"""A few keycodes not defined in curses."""
KEY_ESC = 27
KEY_NUMPAD_PLUS = 465
KEY_NUMPAD_MINUS = 464


class handler_for(object):
    """Decorator class for key handlers."""

    handlers = []  # list of pairs (list of keycodes, handler function)

    def __init__(self, *args):
        self.keycodes = [self.make_keycode(arg) for arg in args]

    def __call__(self, func):
        self.handlers.append((self.keycodes, func))

        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped_func

    @staticmethod
    def make_keycode(key):
        if isinstance(key, int):
            # already a keycode, do nothing
            return key
        elif isinstance(key, str) or isinstance(key, unicode):
            # character: return keycode
            if len(key) > 1:
                raise TypeError('make_keycode() expected a character, but '
                                'string of length {} found'.format(len(key)))
            return ord(key)
        else:
            raise TypeError('make_keycode() expected a string or int, but '
                            '{} found'.format(type(key)))


class CursesApp(object):
    """Main game application.

    Manages the views, handles user input, passes time.
    """

    MIN_SPEED = 0.1   # minimum game speed factor
    MAX_SPEED = 16.0  # maximum game speed factor

    SCREEN_DRAW_FREQ = 30.0  # frequency at which the screen is redrawn

    def __init__(self, game, params, stdscr):
        """Creates a new game application."""

        self.game = game
        self.params = params
        self.screen = stdscr

        self.paused = False
        self.quit = False
        self.speed = 1.0
        self.pos_x, self.pos_y = 0, 0

        self._last_gen_time = time.time()
        self._last_draw_time = time.time()

        self.init_views()

    @handler_for(curses.KEY_RESIZE)
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

        # Reset the grid with initial population
        self.reset()

        # Set non-blocking mode for keyboard events
        self.screen.nodelay(1)
        self.screen.timeout(0)

        # Clear the screen
        self.screen.refresh()

        # First draw
        self.draw()

        # Initialize internal clock
        self._last_gen_time = time.time()
        self._last_draw_time = time.time()

        while not self.quit:
            # Get key press, and pass it to handler.
            keycode = self.screen.getch()
            if keycode != -1:
                for keycodes, func in handler_for.handlers:
                    if keycode in keycodes:
                        func(self)

            # Get current time
            clock = time.time()

            # Is it time for a new generation?
            if clock - self._last_gen_time > 1.0 / self.speed:
                if not self.paused:
                    self.game.next_generation()
                    self._last_gen_time = clock

            # Is it time to redraw the screen?
            if clock - self._last_draw_time > 1.0 / self.SCREEN_DRAW_FREQ:
                self.draw()
                self._last_draw_time = clock

            # Sleep a bit before next iteration
            time.sleep(0)

    def draw(self):
        """Draws the current state of the game."""

        # Draw main window (border, speed, etc.)
        self.game_view.draw(self, self.game)
        self.game_view.refresh(wait=True)

        # Draw the view of the cells
        self.cells_view.draw(self.game, self.pos_x, self.pos_y,
                             self.params['color'])
        self.cells_view.refresh(wait=True)

        # Actually redraw the screen
        curses.doupdate()

    @handler_for('q', KEY_ESC)
    def quit(self):
        self.quit = True

    @handler_for('r')
    def reset(self):
        self.game.reset()
        self.game.populate_random(self.params['prob'])

    @handler_for(' ')
    def pause_unpause(self):
        self.paused = not self.paused

    @handler_for('\n', curses.KEY_ENTER)
    def next_generation(self):
        if self.paused:
            self.game.next_generation()

    @handler_for('+', KEY_NUMPAD_PLUS)
    def increase_speed(self):
        """Increases game speed (if not paused)."""
        if not self.paused:
            self.speed *= 2.0
            if self.speed > self.MAX_SPEED:
                self.speed = self.MAX_SPEED

    @handler_for('-', KEY_NUMPAD_MINUS)
    def decrease_speed(self):
        """Decreases game speed (if not paused)."""
        if not self.paused:
            self.speed /= 2.0
            if self.speed < self.MIN_SPEED:
                self.speed = self.MIN_SPEED

    @handler_for(curses.KEY_LEFT)
    def move_left(self):
        self.pos_x = (self.pos_x - 1) % self.game.width

    @handler_for(curses.KEY_RIGHT)
    def move_right(self):
        self.pos_x = (self.pos_x + 1) % self.game.width

    @handler_for(curses.KEY_UP)
    def move_up(self):
        self.pos_y = (self.pos_y - 1) % self.game.height

    @handler_for(curses.KEY_DOWN)
    def move_down(self):
        self.pos_y = (self.pos_y + 1) % self.game.height
