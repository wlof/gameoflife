#!/usr/bin/env python
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

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from unittest import TestCase, TestSuite, TestLoader, TextTestRunner

from gameoflife.gamepython import GamePython
from gameoflife.gamenumpy import GameNumpy


class GameTestCase(TestCase):
    def setUp(self):
        self.game = self.cls_game(10, 10)

    def tearDown(self):
        pass

    def test_init_cells(self):
        self.game.init_cells()
        for row in range(self.game.width):
            for col in range(self.game.height):
                self.assertTrue(self.game.is_alive(row, col) is False)


class GamePythonTestCase(GameTestCase):
    cls_game = GamePython


class GameNumpyTestCase(GameTestCase):
    cls_game = GameNumpy


def suite():
    suite = TestSuite()
    suite.addTest(TestLoader().loadTestsFromTestCase(GamePythonTestCase))
    suite.addTest(TestLoader().loadTestsFromTestCase(GameNumpyTestCase))
    return suite


if __name__ == '__main__':
    TextTestRunner().run(suite())
