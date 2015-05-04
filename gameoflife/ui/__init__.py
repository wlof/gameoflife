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
from gameoflife.ui.app import CursesApp


def init_colors():
    """Initializes curses colors."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_BLUE, -1)
    curses.init_pair(6, curses.COLOR_CYAN, -1)
    curses.init_pair(7, curses.COLOR_MAGENTA, -1)


def curses_wrapped_main(stdscr, args):
    """curses-wrapped main function."""

    # Set up screen
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # Set up colors if needed
    if args.color == 'auto':
        color = curses.has_colors()
    elif args.color == 'yes':
        color = True
    else:
        color = False

    if color:
        init_colors()

    # Load game implementation according to -n flag
    if args.impl == 'normal':
        from gameoflife.gamepython import GamePython as GameOfLife
    elif args.impl == 'light':
        from gameoflife.gamepython import GamePythonLight as GameOfLife
    elif args.impl == 'numpy':
        from gameoflife.gamenumpy import GameNumPy as GameOfLife
    elif args.impl == 'numpy-light':
        from gameoflife.gamenumpy import GameNumPyLight as GameOfLife

    # Create the game object
    game = GameOfLife(args.width, args.height)

    # Create the game app and start the event loop
    app_params = {'prob': args.prob,
                  'color': color}
    app = CursesApp(game, app_params, stdscr)
    app.main()


def main():
    """Entry point for gameoflife."""

    # Command line argument parser
    parser = ArgumentParser(prog='gameoflife',
                            description="Conway's Game of Life",
                            epilog='Suggestions and bug reports are greatly '
                                   'appreciated: '
                                   'https://github.com/wlof/gameoflife/issues',
                            add_help=False)
    parser.add_argument('--impl', '-i', type=str, default='normal',
                        choices=['normal', 'light',
                                 'numpy', 'numpy-light'],
                        help='game implementation')
    parser.add_argument('--width', '-w', type=int, default=100,
                        help='grid width')
    parser.add_argument('--height', '-h', type=int, default=100,
                        help='grid height')
    parser.add_argument('--prob', '-p', type=float, default=0.5,
                        help='initial population probability')
    parser.add_argument('--color', '-c', type=str, default='auto',
                        choices=['auto', 'yes', 'no'],
                        help='use colors')

    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--help', action='help',
                        help='show this help message and exit')

    # Parse args
    args = parser.parse_args()

    # Parse numpy flag
    if args.impl in ('numpy', 'numpy-light'):
        try:
            imp.find_module('numpy')
        except ImportError:
            parser.error("can't find numpy module. "
                         "Check if NumPy is installed correctly.")

        try:
            imp.find_module('scipy')
        except ImportError:
            parser.error("can't find scipy module. "
                         "Check if SciPy is installed correctly.")

    # Parse dimensions
    if args.width <= 0:
        parser.error('width needs to be a positive integer')
    if args.height <= 0:
        parser.error('height needs to be a positive integer')

    # Parse probability
    if not 0.0 <= args.prob <= 1.0:
        parser.error('probability needs to be between 0.0 and 1.0')

    curses.wrapper(curses_wrapped_main, args)
