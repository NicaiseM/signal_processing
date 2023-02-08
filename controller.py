#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library
from datetime import datetime

# Third-party Libraries

# Own sources
import configurator
from processor import Processor
from abstract_classes import AbstractController


# === Классы ===
class Controller(AbstractController):
    """Класс управления программой."""

    def __init__(self):
        """
        Инициализация контроллера.

        Returns
        -------
        None.

        Notes
        -----
        Как поле текущего класса определяется объект-обработчик,
        загружается словарь конфигурации.

        """
        super().__init__(configurator, Processor)
        self.last_file = None
        self.last_time = datetime.now()

    def processing_start(self, file):
        super().processing_start(file)
        if self.last_file is not self.file:
            self.last_file = self.file
            self.processor.file_processing(self.file)
        else:
            self.processor.file_processing()

    def prepare_none_canvas(self):
        self.canvas['main'] = None

    def cfg_update(self, key, value):
        configurator.configurator.cfg_update(key, value, self.processor.device)
        self.time_now = datetime.now()
        delta = self.time_now - self.last_time
        if self.last_file and delta.total_seconds() >= 0.01:  # Защита
            self.processing_start(self.last_file)
            self.last_time = self.time_now


# === Функции ===

# === Обработка ===
controller = Controller()
if __name__ == '__main__':
    file = r"myFile.csv"
    controller.processing_start(file)
