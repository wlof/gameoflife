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

"""This module contains tne entry point for gameoflife's curses-based UI. To
invoke the UI, just call gameoflife.ui.main().
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import curses
import sys

from gameoflife.game import Game
from gameoflife.ui.app import GameApp
from gameoflife.ui.exceptions import ResizeException


def _raw_main(stdscr, args):
    """curses-wrapped actual main function."""

    # Initialize the colour pairs used by the views.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Set the cursor to be invisible
    curses.curs_set(0)

    # Create the game object
    # For now, dimensions are deduced from terminal size
    height, width = stdscr.getmaxyx()
    game = Game(width, height)

    # Create the game app and start the event loop
    app = GameApp(game, stdscr)
    app.main()


def main(args=None):
    """Entry point for gameoflife. Includes top-level exception handlers that
    print friendly error messages.
    """

    try:
        curses.wrapper(_raw_main, args)
    except ResizeException:
        print("Please do not resize the screen while game is running.",
              file=sys.stderr)
        sys.exit(1)
