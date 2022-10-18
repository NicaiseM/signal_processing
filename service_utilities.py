#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Service utilities

My own service utilities.

"""

# Future
# from __future__ import

# Standard Library
import time

# Third-party Libraries

# Own sources

__author__      = "Nikita Makarchuk"
__copyright__   = "Copyright 2021, Nikita Makarchuk"
__credits__     = ["Nikita Makarchuk"]
__license__     = "GPL"
__version__     = "0.0.1"
__maintainer__  = "Nikita Makarchuk"
__email__       = "nicaise@rambler.ru"
__status__      = "Prototype"


# === Классы ===

class TimeTest:

    def __init__(self):
        self.times = [time.time()]
        self.marks = ['start']

    def point(self, mark):
        if mark != 'end':
            self.times.append(time.time())
            self.marks.append(mark)
        else:
            self.end()

    def end(self):
        self.times.append(time.time())
        self.marks.append('end')
        for i in range(1, len(self.times[1:])):
            print(f'Test №{i} - {self.marks[i]}: '
                  + f'{self.times[i] - self.times[i - 1]:.3f} с;')
        else:
            print('Общее время выполнения программы: '
                  + f'{self.times[-1] - self.times[0]:.3f} с.')


# === Функции ===

# === Обработка ===
