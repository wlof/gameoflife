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

"""This module provides a class that implements the Game of Life using
the NumPy and SciPy libraries.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import numpy as np
from scipy.ndimage.filters import convolve

from gameoflife.game import Game


class GameNumpy(Game):
    """A numpy/scipy based implementation of the Game of Life."""

    def __init__(self, width, height, prob):
        super(GameNumpy, self).__init__(width, height, prob)

        # Weights used for the convolve operation
        self.weights = np.array([[1, 1,  1],
                                 [1, 10, 1],
                                 [1, 1,  1]])

    def init_cells(self):
        """Initializes the grid of cells, and its accompanying grid of
        new cells.
        """
        self.cells = np.zeros((self.width, self.height))
        self.new_cells = np.zeros((self.width, self.height))

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.
        """
        rand = np.random.uniform(0.0, 1.0, (self.width, self.height))
        self.cells = np.int8(rand <= prob)

    def step(self):
        """Computes the next generation of cells based on the current one."""

        # First, we compute the convolved matrix
        con = convolve(self.cells, self.weights, mode='wrap')

        # Here's the trick: we assigned 10 to the central position in the
        # weights matrix. So every entry in the convolved matrix will have
        # values 0-8 for dead cells and 10-18 for live cells, depending on
        # the number of neighbours.
        # The new cells matrix will have a cell for the following values in
        # the convolved matrix:
        # - 3: birth of a new cell
        # - 12 & 13: already live cell, staying alive
        # TODO: use constants, or better yet, make them variables
        boolean = (con == 3) | (con == 12) | (con == 13)
        self.cells = np.int8(boolean)
        self.new_cells = np.int8(con == 3)

    def is_alive(self, row, col):
        """Returns True if there is a live cell at the specified location,
        False if there isn't.
        """
        line = self.cells.take(row, axis=0, mode='wrap')
        cell = line.take(col, mode='wrap')
        return cell == 1

    def is_new(self, row, col):
        """Returns True if there is a live cell that was born with the last
        generation at the specified location, False if there isn't.
        """
        line = self.new_cells.take(row, axis=0, mode='wrap')
        cell = line.take(col, mode='wrap')
        return cell == 1
