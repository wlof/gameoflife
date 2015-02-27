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

"""This module provides the classes used by the pure Python implementation
for managing the cells and their states.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import random


class CircularList(list):
    """Circular list class.

    Permits accessing elements by out-of-range indexing, i.e. indexes are
    modulo'd by the list's length.

    Does not (yet?) support out-of-range splicing.
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
        self.width = width
        self.height = height
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


class CellGrid(TorusGrid):
    """Grid of cells.

    Each position in the grid can have one of two values:
    - True if there is a live cell at this location
    - False if there isn't
    """

    def __init__(self, width, height):
        """Creates a new grid of cells."""
        super(CellGrid, self).__init__(width, height, False)

    def __str__(self):
        s = '\n'.join(['-'.join(['#' if item is True else '-' for item in row])
                       for row in self._rows])
        return s + '\n'

    def populate_random(self, prob=0.5):
        """Populates the grid at random, with specified probability."""
        for row in range(self.height):
            for col in range(self.width):
                self[row][col] = True if random.random() <= prob else False

    def neighbors(self, row, col):
        return [(x, y) for x in range(row - 1, row + 2)
                for y in range(col - 1, col + 2)
                if (row, col) != (x, y)]

    def get_number_neighbors(self, row, col):
        """Returns the number of cells in the Moore neighborhood of the
        specified location.
        """
        number_neighbors = 0
        for x, y in self.neighbors(row, col):
            if self[x][y] is True:
                number_neighbors += 1

        return number_neighbors

    def apply_states(self, states):
        """Kills and spawns cells according to the grid of states."""
        for row in range(self.height):
            for col in range(self.width):
                if states[row][col] in (States.DeathByIsolation,
                                        States.DeathByOverpopulation):
                    self[row][col] = False
                elif states[row][col] == States.Birth:
                    self[row][col] = True


class States:
    """Enumerate of the possible states."""

    NoChange, Birth, DeathByIsolation, DeathByOverpopulation = range(4)


class StateGrid(TorusGrid):
    """Grid of states."""

    N_B = 3      # Number of neighbors needed for a cell to be born
    N_S_MIN = 2  # Minimum number of neighbors needed for a cell to stay alive
    N_S_MAX = 3  # Maximum number of neighbors needed for a cell to stay alive

    def __init__(self, width, height):
        """Creates a grid of states."""
        super(StateGrid, self).__init__(width, height, States.NoChange)

    def __str__(self):
        s = '\n'.join([''.join([str(item) for item in row])
                       for row in self._rows])
        return s + '\n'

    def compute(self, cells):
        """Computes new states according to the grid of cells."""
        for row in range(self.height):
            for col in range(self.width):
                number_neighbors = cells.get_number_neighbors(row, col)

                if cells[row][col] is True:
                    if number_neighbors < StateGrid.N_S_MIN:
                        self[row][col] = States.DeathByIsolation
                    elif number_neighbors > StateGrid.N_S_MAX:
                        self[row][col] = States.DeathByOverpopulation
                    else:
                        self[row][col] = States.NoChange
                else:
                    if number_neighbors == StateGrid.N_B:
                        self[row][col] = States.Birth
                    else:
                        self[row][col] = States.NoChange
