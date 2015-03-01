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


class Fate(object):
    """Enumeration of the possible fates of a cell.

    If the cell is currently dead, it can either stay dead, or be born.
    If the cell is currently alive, it can survive, die by isolation, or
    die by overcrowding.
    """
    StayDead, Birth, Survive, DeathByIsolation, DeathByOvercrowding = range(5)


class GameOfLife(object):
    """Base class for the Game of Life."""

    def __init__(self, width, height):
        """Creates a new instance of the Game of Life."""
        self.width, self.height = width, height
        self.generation = 1
        self._init()

    def _init(self):
        """Initializes whatever internal structures used by the implementation
        to represent cells and compute generations.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def reset(self):
        """Resets the game."""
        self.generation = 1
        self._init()

    def populate_random(self, prob=0.5):
        """Populates the grid of cells at random, with specified
        probability.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def next_generation(self):
        """Triggers the next generation of cells, and increments
        generation.
        """
        self._step()
        self.generation += 1

    def _step(self):
        """Computes the next generation of cells based on the current one.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def fate(self, row, col):
        """Returns the fate of the cell at the specified location.

        Should be implemented by the derived class.
        """
        raise NotImplementedError

    def age(self, row, col):
        """Returns the age of a cell, i.e. how many generations it's been in
        its current state (dead or alive).

        Should be implemented by the derived class.
        """
        raise NotImplementedError
