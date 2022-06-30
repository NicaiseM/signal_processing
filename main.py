#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Обработка осциллографических записей."""

# Future
# from __future__ import

# Standard Library

# Third-party Libraries

# Own sources
import controller


__author__      = "Polina Punina"
__copyright__   = "Copyright 2022, Polina Punina"
__credits__     = ["Polina Punina, Nikita Makarchuck"]
__license__     = "GPL"
__version__     = "0.5.0"
__maintainer__  = "Polina Punina"
__email__       = "nicaise@rambler.ru"
__status__      = "Development"


# === Классы ===

# === Функции ===

# === Обработка ===
ui = ('streamlit', 'pyqt')
controller.controller.run(ui[0])
