#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Хранение словаря метрических коэффициентов

Модуль содержит словарь, позволяющий по показателю степени извлечь
метрический коэффициент и дольные приставки в русском и английском
написании.

"""

# Future
# from __future__ import

# Standard Library

# Third-party Libraries

# Own sources

__author__      = "Nikita Makarchuck"
__copyright__   = "Copyright 2021, Nikita Makarchuck"
__credits__     = ["Nikita Makarchuck"]
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Nikita Makarchuck"
__email__       = "nicaise@rambler.ru"
__status__      = "Production"


# === Обработка ===

metric = {-24: [1e-24, 'и',  'y' ],
          -21: [1e-21, 'з',  'z' ],
          -18: [1e-18, 'а',  'a' ],
          -15: [1e-15, 'ф',  'f' ],
          -12: [1e-12, 'п',  'p' ],
           -9: [1e-9,  'н',  'n' ],
           -6: [1e-6,  'мк', 'µ' ],
           -3: [1e-3,  'м',  'm' ],
           -2: [1e-2,  'с',  'c' ],
           -1: [1e-1,  'д',  'd' ],
            0: [1e0,   '',   ''  ],
            1: [1e1,   'да', 'da'],
            2: [1e2,   'г',  'h' ],
            3: [1e3,   'к',  'k' ],
            6: [1e6,   'М',  'M' ],
            9: [1e9,   'Г',  'G' ],
           12: [1e12,  'Т',  'T' ],
           15: [1e15,  'П',  'P' ],
           18: [1e18,  'Э',  'E' ],
           21: [1e21,  'З',  'Z' ],
           24: [1e24,  'И',  'Y' ]}
