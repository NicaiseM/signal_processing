#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library
import os
from datetime import datetime

# Third-party Libraries

# Own sources
import config
from processor import Processor


# === Классы ===
class Controller():
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
        self.processor = Processor()
        self.cfg = config.configurator.cfg
        self.last_file = None
        self.last_time = datetime.now()

    def run(self, ui):
        """
        Запуск программы.

        Parameters
        ----------
        ui : str
            Тип интерфейса, используемый в программе.

        Returns
        -------
        None.

        Notes
        -----
        В зависимости от аргумента ui программа запускается с тем или
        иным видом интерфейса. Пока есть только streamlit.

        """
        if ui == 'streamlit':
            os.system('streamlit run streamlit_ui.py')
            self.processor.plotter.canvas = None
        elif ui == 'pyqt':
            pass

    def processing_start(self, file):
        if self.last_file is not file:
            self.last_file = file
            self.processor.file_processing(file)
        else:
            self.processor.file_processing()

    def cfg_update(self, key, value):
        config.configurator.cfg_update(key, value, self.processor.device)
        self.time_now = datetime.now()
        delta = self.time_now - self.last_time
        if self.last_file and delta.total_seconds() >= 0.01:  # Защита
            self.processing_start(self.last_file)
            self.last_time = self.time_now

    def cfg_to_default_reset(self):
        config.configurator.cfg_to_default_reset()


# === Функции ===

# === Обработка ===
controller = Controller()
if __name__ == '__main__':
    file = 'test_working_dir/rigol-new/csv/NewFile3.csv'
    controller.processing_start(file)
