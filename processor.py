#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Обработка данных."""

# Future
# from __future__ import

# Standard Library

# Third-party Libraries
import numpy as np

# Own sources
import config
from opener import Opener
from plotter import Plotter
from metric import metric as mt


# === Классы ===
class Processor():
    """Класс - обработчик данных."""

    def __init__(self):
        self.opener = Opener()
        self.plotter = Plotter()
        self.device = None

    def data_updating(self, file):
        if file:
            self.raw_data, self.t_step, self.device, self.ch_num \
                = self.opener.open(file[0])
        self.data = self.raw_data.copy()
        self.cfg = config.configurator.device_cfg_extract('processing',  # !!! Что делать, если не назначен прибор?
                                                          device=self.device)
        for key, value in config.configurator.cfg['metric'].items():
            self.cfg[key] = value

    def file_processing(self, *file):
        if not file:
            file = None
        self.data_updating(file)
        self.invert(self.data)
        if self.cfg['time_shift']:
            self.time_shift_removal(self.data, 0)
        if self.cfg['channel_shift']:
            self.channel_shift_removal(self.data,
                                       self.cfg['channel_shift_amount'])
        if self.cfg['time_limitation']:
            self.time_limitation(self.data, self.cfg['time_limits'])
        if self.cfg['moving_average_smoothing']:
            self.moving_average_smoothing(self.data,
                                          self.cfg['moving_average_window'])
        self.plotter.plotting(self.data[0], self.data[1], self.data[2],
                              mt[self.cfg['t_mt_factor']],
                              mt[self.cfg['ch1_mt_factor']],
                              mt[self.cfg['ch2_mt_factor']])

    def invert(self, data):
        """
        Инвертирование каналов.

        Parameters
        ----------
        data : array
            Массив NumPy, содержащий обрабатываемые данные.

        Returns
        -------
        None.

        Notes
        -----
        Определяются коэффициенты инвертирования согласно bool
        аргументам invert словаря настроек, после выполняется
        инвертирование умножением на 1 или -1.

        """
        # Коэффициенты инвертирования каналов: 1 когда False, -1 когда True
        invert = [1 - 2*i for i in self.cfg['invert']]
        for num, channel in enumerate(data[1:]):
            channel *= invert[num]

    def time_shift_removal(self, data, zero_time):
        """
        Ликвидация сдвига по времени.

        Parameters
        ----------
        data : array
            Массив NumPy, содержащий обрабатываемые данные.
        zero_time : int or float
            Значение времени, принимаемое за ноль.

        Returns
        -------
        None

        Notes
        -----
        Функция определяет сдвиг по времени как поданное на ввод
        значение и для каждого элемента производит вычитание этого
        значения.

        """
        time_shift = data[0][0] - zero_time
        data[0] -= time_shift

    def channel_shift_removal(self, data, amount=1000):
        """
        Ликвидация сдвига нуля исследуемой величины.

        Parameters
        ----------
        data : array
            Массив NumPy, содержащий обрабатываемые данные.
        amount : int
            Количество проходов по определению сдвига.

        Returns
        -------
        None

        Notes
        -----
        Функция определяет значение сдвига как среднее первых amount
        значений массива сигнала, после чего для каждого элемента
        производит вычитание этого значения.

        """
        for channel in data[1:]:
            shift = np.mean(channel[:amount])
            channel -= shift

    def time_limitation(self, data, time_limits):
        """
        Сглаживание скользящей средней.

        Parameters
        ----------
        data : array
            Массив NumPy, содержащий обрабатываемые данные.
        time_limits : tuple of int or float
            Нижняя и верхняя границы по времени.

        Returns
        -------
        None

        Notes
        -----
        Отсутствующие границы задаются как NaN, т.к. yaml понимает NaN
        при конвертации значений во float, но не понимает None.
        Отсутствующие границы заменяются минимальным и максимальным
        значением массива времени соответственно. Определяется массив
        логических индексов под условие соответствия границам, после
        по этому массиву берется срез по всем строкам data.

        """
        if np.isnan(time_limits[0]):
            time_limits[0] = np.min(data)
        if np.isnan(time_limits[1]):
            time_limits[1] = np.max(data)
        ind = (time_limits[0] <= data[0]) & (data[0] <= time_limits[1])
        self.data = data[:, ind]

    def moving_average_smoothing(self, data, window=10):
        """
        Сглаживание методом скользящей средней.

        Parameters
        ----------
        data : array
            Массив NumPy, содержащий обрабатываемые данные.
        window : int
            Ширина окна сглаживания.

        Returns
        -------
        None

        Returns
        -------
        None

        Notes
        -----
        Метод находит среднее значение исследуемого сигнала на ширине
        окна и подставляет его вместо исходного. В процессе цикла функция
        проходит по всем точкам последовательности, не затрагивая только
        участки в начале и в конце массива.

        """
        for channel in data[1:]:
            for i in range(window, channel.size - window):
                window_sum = 0
                for j in range(-window, window + 1):
                    window_sum += channel[i + j]
                channel[i] = (window_sum/(2*window + 1))


# === Функции ===

# === Обработка ===
if __name__ == '__main__':
    file = 'test_working_dir/rigol-new/csv/NewFile3.csv'
    processor = Processor()
    processor.file_processing(file)
