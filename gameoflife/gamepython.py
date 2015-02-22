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

"""This module provides a class that implements the Game of Life in pure
Python.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from gameoflife.game import Game
from gameoflife.grids import CellGrid, StateGrid, States


class GamePython(Game):
    """A pure Python implementation of the Game of Life."""

    def init_cells(self):
        """Initializes the grid of cells, and its accompanying grid of
        states.
        """
        self.cells = CellGrid(self.width, self.height)
        self.states = StateGrid(self.width, self.height)

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.
        """
        self.cells.populate_random(prob)

    def step(self):
        """Computes the next generation of cells based on the current one."""

        # First, we compute the states according to the current generation of
        # cells
        self.states.compute(self.cells)

        # Then we apply the states to the cells to get the next generation
        self.cells.apply_states(self.states)

    def is_alive(self, row, col):
        """Returns True if there is a live cell at the specified location,
        False if there isn't.
        """
        return self.cells[row][col] is True

    def is_new(self, row, col):
        """Returns True if there is a live cell that was born with the last
        generation at the specified location, False if there isn't.
        """
        return self.states[row][col] == States.Birth
