#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Обработка осциллографических записей."""

# Future
# from __future__ import

# Standard Library

# Third-party Libraries

# Own sources
from controller import Controller


__author__      = "Nikita Makarchuck"
__copyright__   = "Copyright 2021, Nikita Makarchuck"
__credits__     = ["Nikita Makarchuck"]
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Nikita Makarchuck"
__email__       = "nicaise@rambler.ru"
__status__      = "Prototype|Development|Production"


# === Классы ===

# === Функции ===

# === Обработка ===
ui = ('streamlit', 'pyqt')
controller = Controller()
controller.run(ui[0])

# TODO
    # открытие файлов - доработать
    # обработка
    # графопостроение
