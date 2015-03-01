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

from gameoflife.gameoflife import GameOfLife, Fate


class BaseGameNumPy(GameOfLife):
    """Base class for both Numpy/SciPy implementations."""

    # Weights used for the convolve operation
    WEIGHTS = np.array([[1, 1,  1],
                        [1, 10, 1],
                        [1, 1,  1]])

    def _init(self):
        """Initializes the internal structures used by the implementation."""

        # Cells grid. Each item is either 0 for a dead cell or 1 for a live
        # one.
        self.cells = np.zeros((self.width, self.height), dtype=np.int8)

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.
        """
        rand = np.random.uniform(0.0, 1.0, (self.width, self.height))
        self.cells = np.int8(rand <= prob)


class GameNumPy(BaseGameNumPy):
    """Full-featured NumPy/SciPy-based implementation of the Game of Life."""

    def _init(self):
        """Initializes the internal structures used by the implementation."""
        super(GameNumPy, self)._init()

        # Fates grid. Each item contains the fate of the cell at the location
        # for the next generation.
        self.fates = np.zeros((self.width, self.height), dtype=np.int8)
        self.fates.fill(Fate.StayDead)

        # Ages grid. Each item is the number of generations the cell at the
        # location has been in its current state (dead or alive).
        self.ages = np.zeros((self.width, self.height), dtype=np.int64)

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.
        """
        super(GameNumPy, self).populate_random(prob)
        self._compute_fates()

    def _step(self):
        """Computes the next generation of cells based on the current one."""
        self._apply_fates()
        self._compute_fates()

    def fate(self, row, col):
        """Returns the fate of the cell at the specified location."""
        line = self.fates.take(row, axis=0, mode='wrap')
        fate = line.take(col, mode='wrap')
        return fate

    def age(self, row, col):
        """Returns the age of a cell, i.e. how many generations it's been in
        its current state (dead or alive).
        """
        line = self.ages.take(row, axis=0, mode='wrap')
        age = line.take(col, mode='wrap')
        return age

    def _compute_fates(self):
        """Computes the fate of all cells."""

        # Compute the convolved matrix of neighbors
        con = convolve(self.cells, self.WEIGHTS, mode='wrap')

        # Here's the trick: we assigned 10 to the central element of the
        # weights kernel. Therefore, currently dead cells will have a value
        # of 0-8 in the convolved matrix, and currently live cells will have
        # a value of 10-18 (depending on the number of neighbors).

        # Reset the fates grid
        self.fates.fill(Fate.StayDead)

        # Dead cells with exactly 3 neighbors will be born
        self.fates[con == 3] = Fate.Birth

        # Live cells with less than 2 neighbors will die by isolation
        self.fates[(con >= 10) & (con < 12)] = Fate.DeathByIsolation

        # Live cells with 2 or 3 neighbors survive
        self.fates[(con == 12) | (con == 13)] = Fate.Survive

        # Live cells with more than 3 neighbors die by overcrowding
        self.fates[con > 13] = Fate.DeathByOvercrowding

    def _apply_fates(self):
        """Applies the fates to all cells."""

        # The new cells grid has live cells for every "birth" or "survive"
        # fates, and dead cells for everything else
        new_cells = np.zeros((self.width, self.height), dtype=np.int8)
        new_cells[(self.fates == Fate.Birth) |
                  (self.fates == Fate.Survive)] = 1

        # Check which cells have changed (dead to live or vice-versa)
        unchanged = new_cells == self.cells
        changed = np.logical_not(unchanged)

        # Unchanged cells grow one generation older, changed cells have their
        # ages reset to zero
        self.ages[unchanged] += 1
        self.ages[changed] = 0

        # Memorize the new cells grid
        self.cells = new_cells


class GameNumPyLight(BaseGameNumPy):
    """Light version of the NumPy/SciPy-based implementation of the Game of
    Life.
    """

    def _step(self):
        """Computes the next generation of cells based on the current one."""

        # Compute the convolved matrix of neighbors
        con = convolve(self.cells, self.WEIGHTS, mode='wrap')

        # The trick is the same as in the full-featured version, but we don't
        # need to track fates, so we can simply set the new live cells to be:
        # - currently dead cells with exactly 3 neighbors, and
        # - currently live cells with 2 or 3 neighbors
        self.cells.fill(0)
        self.cells[(con == 3) | (con == 12) | (con == 13)] = 1

    def fate(self, row, col):
        """Returns the fate of the cell at the specified location."""

        # The light implementation does not know the fates, so it cheats by
        # returning "survive" for all currently live cells and "stay dead" for
        # all currently dead cells.
        line = self.cells.take(row, axis=0, mode='wrap')
        cell = line.take(col, mode='wrap')
        return Fate.Survive if cell == 1 else Fate.StayDead

    def age(self, row, col):
        """Returns the age of a cell, i.e. how many generations it's been in
        its current state (dead or alive).
        """

        # The light implementation does not know the ages, so it cheats and
        # returns a constant value.
        return 1000
