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

"""This module provides the base class for the Game of Life."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class Game(object):
    """Base class for the Game of Life."""

    def __init__(self, width, height, prob):
        """Creates a new instance of the Game of Life."""
        self.width, self.height = width, height
        self.prob = prob

        self.generation = 1

        self.init_cells()

    def init_cells(self):
        """Initializes the grid of cells.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def reset(self):
        """Resets the game, i.e. repopulates it at random and goes back to
        generation 1.
        """
        self.populate_random(self.prob)
        self.generation = 1

    def step(self):
        """Computes the next generation of cells based on the current one.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def next_generation(self):
        """Triggers the next generation of cells, and increments
        generation.
        """
        self.step()
        self.generation += 1

    def is_alive(self, row, col):
        """Returns True if there is a live cell at the specified location,
        False if there isn't.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def is_new(self, row, col):
        """Returns True if there is a live cell that was born with the last
        generation at the specified location, False if there isn't.

        Should be implemented by the derived class.
        """
        raise NotImplementedError
