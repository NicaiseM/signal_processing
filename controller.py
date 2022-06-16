#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library
import os

# Third-party Libraries

# Own sources
from processor import Processor


# === Классы ===
class Controller():
    """Класс управления программой."""

    def __init__(self):
        self.processor = Processor()
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

    def processing_start(self, cfg_in, file):
        if file == self.last_file:
            self.processor.file_processing(cfg_in)
        else:
            self.last_file = file
            self.processor.file_processing(cfg_in, file)

# === Функции ===

# === Обработка ===
