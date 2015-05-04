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

import random

from gameoflife.gameoflife import GameOfLife, Fate


class CircularList(list):
    """Circular list class.

    Permits accessing elements by out-of-range indexing, i.e. indexes are
    modulo'd by the list's length.
    """

    def __getitem__(self, key):
        return list.__getitem__(self, key % len(self))

    def __setitem__(self, key, value):
        list.__setitem__(self, key % len(self), value)


class TorusGrid(object):
    """A grid whose edges are connected.

    Basically, a circular 2D array. Dimensions are set at construction time.
    """

    def __init__(self, width, height, init_value=0):
        """Creates a new grid with specified dimensions."""
        self._rows = [CircularList([init_value] * width)
                      for _ in range(height)]

    def __getitem__(self, idx):
        return self._rows[idx % len(self._rows)]

    def __setitem__(self, idx, value):
        self._rows[idx % len(self._rows)] = value

    def __str__(self):
        s = '\n'.join([' '.join([str(item) for item in row])
                       for row in self._rows])
        return s + '\n'


class BaseGamePython(GameOfLife):
    """Base class for both pure Python implementations."""

    def _init(self):
        """Initializes the internal structures used by the implementation."""

        # Cells grid. Each item is either 0 for a dead cell or 1 for a live
        # one.
        self.cells = TorusGrid(self.width, self.height, 0)

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.
        """
        for row in range(self.height):
            for col in range(self.width):
                self.cells[row][col] = 1 if random.random() <= prob else 0

    @staticmethod
    def coords_neighbors(row, col):
        """Returns the coordinates for the neighbors of the specified
        location.
        """
        for x in range(row - 1, row + 2):
            for y in range(col - 1, col + 2):
                if (row, col) != (x, y):
                    yield (x, y)

    def get_number_neighbors(self, row, col):
        """Returns the number of live cells in the Moore neighborhood on the
        specified location.
        """
        num_neighbors = 0
        for x, y in self.coords_neighbors(row, col):
            if self.cells[x][y] == 1:
                num_neighbors += 1
        return num_neighbors


class GamePython(BaseGamePython):
    """Full-featured pure Python implementation of the Game of Life."""

    def _init(self):
        """Initializes the internal structures used by the implementation."""
        super(GamePython, self)._init()

        # Fates grid. Each item contains the fate of the cell at the location
        # for the next generation.
        self.fates = TorusGrid(self.width, self.height, Fate.StayDead)

        # Ages grid. Each item is the number of generations the cell at the
        # location has been in its current state (dead or alive).
        self.ages = TorusGrid(self.width, self.height, 0)

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.
        """
        super(GamePython, self).populate_random(prob)
        self.ages = TorusGrid(self.width, self.height, 0)
        self._compute_fates()

    def _step(self):
        """Computes the next generation of cells based on the current one."""
        self._apply_fates()
        self._compute_fates()

    def fate(self, row, col):
        """Returns the fate of the cell at the specified location."""
        return self.fates[row][col]

    def age(self, row, col):
        """Returns the age of a cell, i.e. how many generations it's been in
        its current state (dead or alive).
        """
        return self.ages[row][col]

    def _compute_fates(self):
        """Computes the fate of all cells."""
        for row in range(self.height):
            for col in range(self.width):
                num_neighbors = self.get_number_neighbors(row, col)

                if self.cells[row][col] == 0:
                    # Currently dead cell
                    if num_neighbors == 3:
                        # Exactly 3 neighbors: a new cell is born!
                        self.fates[row][col] = Fate.Birth
                    else:
                        # Otherwise: the cell stays dead
                        self.fates[row][col] = Fate.StayDead
                else:
                    # Currently live cell
                    if num_neighbors < 2:
                        # Not enough neighbors: death by isolation
                        self.fates[row][col] = Fate.DeathByIsolation
                    elif num_neighbors > 3:
                        # Too many neighbors: death by overcrowding
                        self.fates[row][col] = Fate.DeathByOvercrowding
                    else:
                        # Just the right number of neighbors: survive
                        self.fates[row][col] = Fate.Survive

    def _apply_fates(self):
        """Applies the fates to all cells."""
        for row in range(self.height):
            for col in range(self.width):
                if self.fates[row][col] in (Fate.StayDead, Fate.Survive):
                    self.ages[row][col] += 1
                else:
                    self.ages[row][col] = 0
                    if self.fates[row][col] == Fate.Birth:
                        self.cells[row][col] = 1
                    else:
                        self.cells[row][col] = 0


class GamePythonLight(BaseGamePython):
    """Light version of the pure Python implementation of the Game of Life."""

    def _step(self):
        """Computes the next generation of cells based on the current one."""
        new_cells = TorusGrid(self.width, self.height, 0)

        for row in range(self.height):
            for col in range(self.width):
                num_neighbors = self.get_number_neighbors(row, col)

                if (self.cells[row][col] == 0 and num_neighbors == 3) or \
                   (self.cells[row][col] == 1 and (2 <= num_neighbors <= 3)):
                    new_cells[row][col] = 1
                else:
                    new_cells[row][col] = 0

        self.cells = new_cells

    def fate(self, row, col):
        """Returns the fate of the cell at the specified location."""

        # The light implementation does not know the fates, so it cheats by
        # returning "survive" for all currently live cells and "stay dead" for
        # all currently dead cells.
        return Fate.Survive if self.cells[row][col] == 1 else Fate.StayDead

    def age(self, row, col):
        """Returns the age of a cell, i.e. how many generations it's been in
        its current state (dead or alive).
        """

        # The light implementation does not know the ages, so it cheats and
        # returns a constant value.
        return 1000
