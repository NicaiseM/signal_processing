#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library
import os

# Third-party Libraries

# Own sources
import config
from processor import Processor


# === Классы ===
class Controller():
    """Класс управления программой."""

    def __init__(self):
        self.processor = Processor()
        self.configurator = config.configurator
        self.last_file = None

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
        elif ui == 'pyqt':
            pass

    def processing_start(self, file):
        self.processor.file_processing(file)

# === Функции ===

# === Обработка ===
