#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from gameoflife import __version__


setup(name='gameoflife',
      version=__version__,
      license='MIT',
      description="Conway's Game of Life",
      long_description=open('README.md').read(),
      keywords='gameoflife game of life conway',
      url='https://github.com/wlof/gameoflife',
      author='wlof',
      author_email='wlof42@gmail.com',
      packages=find_packages(),
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3'],
      entry_points={
          'console_scripts': ['gameoflife = gameoflife.ui:main']
      })
