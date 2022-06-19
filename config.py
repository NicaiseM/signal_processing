#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Сбор конфигурации из файлов в один модуль."""

# Future
# from __future__ import

# Standard Library

# Third-party Libraries

# Own sources
import yaml


# === Классы ===
class Configurator():
    """Класс формирования конфигурации."""

    def __init__(self):
        with open('./config_default.yml') as f:
            self.default_cfg = yaml.safe_load(f)
            self.cfg = self.default_cfg


# === Функции ===

# === Обработка ===
configurator = Configurator()
cfg = configurator.cfg.copy()  # Заглушка для исполнения остального кода
