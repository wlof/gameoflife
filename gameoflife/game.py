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

"""This module provides the main game class."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from gameoflife.grids import CellGrid, StateGrid


class Game(object):
    """Main class."""

    def __init__(self, width, height):
        """Creates a new instance of the game of life."""
        self.width, self.height = width, height

        self.generation = 1

        # Instantiate cell grid and populates it at random
        self.cells = CellGrid(self.width, self.height)
        self.cells.populate_random()

        # Instantiate state grid
        self.states = StateGrid(self.width, self.height)

    def reset(self):
        """Resets the game."""

        # Save pause state and pause during the reset
        pause_state = self.paused
        self.paused = True

        # Resets grids
        self.cells = CellGrid(self.world_width, self.world_height)
        self.cells.populate_random()
        self.states = StateGrid(self.world_width, self.world_height)
        self.generation = 1

        # Restore pause state
        self.paused = pause_state

    def next_generation(self):
        """Triggers the next generation of cells."""
        self.states.compute(self.cells)
        self.cells.apply_states(self.states)
        self.generation += 1
