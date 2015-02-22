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

"""This module contains the entry point for gameoflife's curses-based UI. To
invoke the UI, just call gameoflife.ui.main().
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import curses
import imp
from argparse import ArgumentParser

from gameoflife import __version__
from gameoflife.ui.app import GameApp


def _curses_wrapped_main(stdscr, args):
    """curses-wrapped main function."""

    # Initialize the colour pairs used by the views.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Set the cursor to be invisible
    curses.curs_set(0)

    # Load game implementation according to -n flag
    if args.numpy:
        from gameoflife.gamenumpy import GameNumpy as Game
    else:
        from gameoflife.gamepython import GamePython as Game

    # Create the game object
    game = Game(args.width, args.height)

    # Create the game app and start the event loop
    app = GameApp(game, stdscr)
    app.main()


def main():
    """Entry point for gameoflife."""

    # Command line argument parser
    parser = ArgumentParser(prog='gameoflife',
                            description="Conway's Game of Life",
                            epilog='Suggestions and bug reports are greatly appreciated: '
                                   'https://github.com/wlof/gameoflife/issues', add_help=False)
    parser.add_argument('--numpy', '-n', action='store_true',
                        help='use the Numpy implementation')
    parser.add_argument('--width', '-w', type=int, default=100,
                        help='grid width')
    parser.add_argument('--height', '-h', type=int, default=100,
                        help='grid height')

    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--help', action='help', help='show this help message and exit')

    # Parse args
    args = parser.parse_args()

    # Parse numpy flag
    if args.numpy:
        try:
            imp.find_module('numpy')
        except ImportError:
            parser.error('numpy import failed. Check if numpy is installed correctly.')

        try:
            imp.find_module('scipy')
        except ImportError:
            parser.error('scipy import failed. Check if scipy is installed correctly.')

    # Parse dimensions
    if args.width <= 0:
        parser.error('width needs to be a positive integer')
    if args.height <= 0:
        parser.error('height needs to be a positive integer')

    curses.wrapper(_curses_wrapped_main, args)
