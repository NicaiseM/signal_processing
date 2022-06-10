#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Чтение данных из csv-файлов."""

# Future
# from __future__ import

# Standard Library
import os
import time
from pathlib import Path

# Third-party Libraries
import scipy
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Own sources
from exceptions import WrongCsvStructureError
from config import cfg


class Opener:
    """Класс-импортер данных из csv-файлов."""

    def __init__(self, *args, **kwargs):
        self.set_cfg()

    def set_cfg(self):
        """
        Создание поля с сигнатурами записей различных приборов.

        Returns
        -------
        None.

        """
        self.cfg = cfg['devices']

    def read(self, file):
        """
        Чтение данных из csv-файла.

        Parameters
        ----------
        file : str
            Адрес обрабатываемого файла.

        Returns
        -------
        data : array
            Массив данных.
        t_step : float
            Шаг времени между выборками.
        recorder_device : str
            Название прибора, записавшего файл.
        two_channels : bool
            Наличие двухканальной записи в файле.

        Notes
        -----
        Производится попытка открыть файл по адресу file, в случае
        неудачи вызывается исключение FileNotFoundError Открытие
        текстового файла на чтение производится посредством функции
        with(), что позволяет быть уверенным в том, что файл будет
        закрыт независимо от результатов работы программы. Первая
        строка каждого файла схраняется. Первая строка будет уникальной
        для каждого осциллографа, и, посредством сравнения строки,
        считанной из файла, с образцами из словаря self.cfg происходит
        определение прибора, сформировавшего обрабатываемый файл.
        оложение образца-сигнатуры в первой строке файла также задается
        в self.cfg и преобразуется в объект-срез, который применяется к
        текстовой строке. Сравнение происходит с образцами
        одноканальных и двухканальных записей, результат сравнения
        определяет также количество каналов. Если происходит
        совпадение, то сохраняется название прибора, записавшего файл,
        и цикл прекращается. Далее данные считываются из файла при
        помощи метода extract. Если совпадения нет, то вызывается
        исключение WrongCsvStructureError.

        """
        recorder_device = None
        two_channels = False
        try:
            with open(file, 'r') as file:
                test_line = file.readline()

                for device in self.cfg:
                    position = slice(device['position'])
                    if test_line[position] == device['signature_1ch']:
                        recorder_device = device
                        break
                    elif test_line[position] == device['signature_2ch']:
                        recorder_device = device
                        two_channels = True
                        break
                else:
                    if recorder_device is None:
                        raise WrongCsvStructureError  # TODO: Возвращение в цикл
                data, t_step = self.extract(file, device['invert'],
                                            recorder_device, two_channels)
        except FileNotFoundError:
            pass  # TODO: Возвращение в цикл
        return data, t_step, recorder_device, two_channels

    def extract(self, file, invert, device, two_channels):
        """
        Извлечение данных из csv-файла.

        Parameters
        ----------
        file : str
            Адрес обрабатываемого файла.
        invert : list of bool
            Наличие необходимости в инвертировании для каналов.
        device : str
            Название прибора, записавшего файл
        two_channels : bool
            Наличие двухканальной записи в файле.

        Returns
        -------
        data : array
            Массив данных.
        t_step : float
            Шаг времени между выборками.

        Notes
        -----
        Создается словарь data и список имен каналов names. Если канал
        один, то names ограничивается справа. Определяются коэффициенты
        инвертирования согласно bool аргументам invert, при этом первый
        столбец данных (время) не инвертируется. Дальнейшее поведение
        зависит от записывающего прибора. В общем случае метод
        считывает данные из файла посредством команды read_csv модуля
        Pandas, при этом указывается запрет на автоматическую
        индексацию, столбцам присваиваются имена, пропускается
        определенное число строк в начале документа и импорту
        подвергаются только указанные строки. Результатом импорта
        становится объект DataFrame, из него извлекаются массивы Numpy
        и помещаются в словарь data под соответствующими именами.
        Одновременно выполняется инвертирование умножением на 1 или -1.
        Также для осциллографа Rigol MSO1104Z/DS1074Z требуются
        дополнительные параметры времени. Время в файлах данного
        формата представлено в виде значений шага и стартового времени,
        т.е. показания представлены в виде трио номер-ch1-ch2. Для
        получения начала и шага считывается вторая строка. После
        значения времени вычисляем в соответствии с этими параметрами.
        Для Micsig из файла извлекается величина задержки, после чего
        подсчитывается настоящее время, т.к. Miqsig записывает время
        относительно опорной точки (см. руководство к осциллографу).
        После определяется шаг времени и происходит переупаковка
        словаря data в двухмерный массив Numpy, где нулевой строкой
        становится время, первой (и второй, если есть второй канал) -
        соответствующие значения измеренных величин.

        """
        data = {}
        t_step = None
        names = ['t', 'ch1', 'ch2']
        if not two_channels:
            names = names[:-1]
        # Коэффициенты инвертирования каналов: 1 когда False, -1 когда True
        invert = [1] + [1 - 2*i for i in invert]

        if device == 'Globaltest':
            df = pd.read_csv(file, index_col=False, names=names, sep='\t')
            for num, name in enumerate(names):
                data[name] = df[name].values*invert[num]
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])
            # FIXME Сделать адекватную нормализацию
            for i in range(len(data['t']) - 1):
                data['t'][i + 1] = data['t'] + t_step

        elif device == 'Gydropribor':
            df = pd.read_csv(file, index_col=False, names=names, sep='\s+')
            for name in names:
                data[name] = df[name].values*invert[num]
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])
            # !!! TODO Проверить необходимость добавления фиксированного шага

        elif device == 'Micsig tBook':
            usecols = [3, 4, 10]
            if not two_channels:
                usecols = usecols[:-1]
            df = pd.read_csv(file, index_col=False, names=names,
                             skiprows=13, usecols=usecols)
            for name in names:
                data[name] = df[name].values*invert[num]
            delay = np.loadtxt(file, delimiter=',', dtype='str',
                               skiprows=5, max_rows=1, usecols=1)
            delay = float(np.ndarray.item(delay).split(' ')[0])
            data['t'] = data['t'] - ((data['t'][-1] - data['t'][0])/2 - delay)
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])

        elif device == 'Rigol MSO1104Z/DS1074Z':
            params = list(map(float, file.readline().split(',')[2:]))
            t_start, t_step = params[0], params[1]
            df = pd.read_csv(file, index_col=False, names=names)
            for name in names:
                data[name] = df[name].values*invert[num]
            data['t'] = t_start + t_step*data['t'].values

        elif device == 'Rigol DS1102E':
            df = pd.read_csv(file, index_col=False, names=names,
                             delimiter=',', skiprows=1)
            for name in names:
                data[name] = df[name].values*invert[num]
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])

        elif device == 'Rigol (unknown)':
            params = file.readline().split('\t')[2:]
            params = [float(i.replace(',', '.')) for i in params]
            t_start, t_step = params[0], params[1]
            df = pd.read_csv(file, index_col=False, names=names,
                             delimiter='\t', decimal=',')
            for name in names:
                data[name] = df[name].values*invert[num]
            data['t'] = t_start + t_step*data['t'].values

        elif device == 'Tektronix MSO46':
            df = pd.read_csv(file, index_col=False, names=names, skiprows=12)
            for name in names:
                data[name] = df[name].values*invert[num]

        if not two_channels:
            data = np.array([data['t'], data['ch1']])
        else:
            data = np.array([data['t'], data['ch1'], data['ch1']])
        return data, t_step

        # TODO 'Tektronix TDS1012B', 'Tektronix TDS2012C'
        # Код из программы обработки шокеров
        #
        # elif (signature.split('\t')[0] == 'Record Length'
        #       and device == 'Tektronix TDS1012B'):
        #     params = pd.read_csv(f, sep='\t', usecols=[0, 1], nrows=16,
        #                          index_col=0, names=['key', 'value'])
        #     params = params.dropna().to_dict()['value']
        #     str_to_float(params)
        #     with open(file, 'r') as f1:
        #         df = pd.read_csv(f1, index_col=False, names=['t', 'ch'],
        #                          sep='\t', usecols=[3, 4], dtype=float)
        #         ch = df['ch'].values
        #         time = df['t'].values
        #     ch = ((ch/params['Probe Atten'] - params['Vertical Offset'])
        #           *params['Vertical Scale'])
        #     time = time*params['Horizontal Scale']/1e12
        #     x_step = params['Sample Interval']

        # elif (signature.split(',')[0] == 'Record Length'
        #       and device == 'Tektronix TDS2012C'):
        #     params = pd.read_csv(f, sep=',', usecols=[0, 1], nrows=16,
        #                          index_col=0, names=['key', 'value'])
        #     params = params.dropna().to_dict()['value']
        #     str_to_float(params)
        #     with open(file, 'r') as f1:
        #         df = pd.read_csv(f1, index_col=False, names=['t', 'ch'],
        #                          sep=',', usecols=[3, 4], dtype=float)
        #         ch = df['ch'].values
        #         time = df['t'].values
        #     x_step = params['Sample Interval']
