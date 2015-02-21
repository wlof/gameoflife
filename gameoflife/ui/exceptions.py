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

"""This module contains tne entry point for gameoflife's curses-based UI. To
invoke the UI, just call gameoflife.ui.main().
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class ResizeException(Exception):
    """Exception class to handle (or rather, not handle) resize events."""
