#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Чтение данных из csv-файлов."""

# Future
# from __future__ import

# Standard Library
from io import StringIO

# Third-party Libraries
import numpy as np
import pandas as pd
from streamlit.elements.file_uploader import UploadedFile

# Own sources
import configurator
from exceptions import WrongCsvStructureError


# === Классы ===
class Opener:
    """Класс - импортер данных из csv-файлов."""

    def __init__(self):
        """
        Инициализация открывашки.

        Returns
        -------
        None.

        Notes
        -----
        Из словаря конфигурации извлекаются настройки, связанные с
        открытием файлов.

        """
        self.cfg = configurator.configurator.device_cfg_extract('reading')

    def open(self, file, recorder_device=None, ch_num=None):
        """
        Открытие csv-файла на чтение.

        Parameters
        ----------
        file : str or PathLike or UploadedFile
            Адрес обрабатываемого файла.
        recorder_device : str
            Название прибора, записавшего файл.
        ch_num : int
            Число каналов в файле.

        Returns
        -------
        data : array
            Массив данных.
        t_step : float
            Шаг времени между выборками.
        recorder_device : str
            Название прибора, записавшего файл.
        ch_num : int
            Число каналов в файле.

        Notes
        -----
        Производится попытка открыть файл по адресу file, в случае
        неудачи вызывается исключение FileNotFoundError Производится
        проверка, является ли файл объектом UploadedFile, который
        образуется при использовании st.file_uploader модуля Streamlit.
        В этом случае файл уже открыт и записан в оперативной памяти,
        он преобразуется в строку иструментом StringIO. Иначе открытие
        текстового файла на чтение производится посредством функции
        with(), что позволяет быть уверенным в том, что файл будет
        закрыт независимо от результатов работы программы. Независимо
        от способа открытия далее файл считывается методом read.
        Аргументы recorder_device и ch_num опциональны. Если они не
        заданы, то определение прибора и числа каналов производится
        в методе read.

        """
        self.recorder_device = recorder_device
        self.ch_num = ch_num
        if isinstance(file, UploadedFile):
            file = StringIO(file.getvalue().decode('utf-8'), newline=None)
            data, t_step = self.read(file)
        else:
            try:
                with open(file, 'r', encoding='utf-8') as file:
                    data, t_step = self.read(file)
            except FileNotFoundError:
                pass
                # return  # TODO Возвращение в цикл
        return data, t_step, self.recorder_device, self.ch_num

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

        Notes
        -----
        На вход метода подается файл в открытом текстовом виде Первая
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
        и цикл прекращается. Далее данные извлекаются из файла при
        помощи метода extract. Если совпадения нет, то вызывается
        исключение WrongCsvStructureError.

        """
        test_line = file.readline()
        if not self.recorder_device:
            self.ch_num = 1
            for device in self.cfg:
                position = slice(*self.cfg[device]['position'])
                if test_line[position] == (self.cfg[device]
                                           ['signature_1ch']):
                    self.recorder_device = device
                    break
                elif test_line[position] == (self.cfg[device]
                                             ['signature_2ch']):
                    self.recorder_device = device
                    self.ch_num += 1
                    break
            else:
                if self.recorder_device is None:
                    position = slice(
                        *self.cfg['Rigol DS1000Z Series']['position'])
                    raise WrongCsvStructureError
                    return  # TODO: Возвращение в цикл
        data, t_step = self.extract(file)
        return data, t_step

    def extract(self, file):
        """
        Извлечение данных из csv-файла.

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

        Notes
        -----
        Создается словарь data и список имен каналов names. Если канал
        один, то names ограничивается справа. Дальнейшее поведение
        зависит от записывающего прибора. В общем случае метод
        считывает данные из файла посредством команды read_csv модуля
        Pandas, при этом указывается запрет на автоматическую
        индексацию, столбцам присваиваются имена, пропускается
        определенное число строк в начале документа и импорту
        подвергаются только указанные строки. Результатом импорта
        становится объект DataFrame, из него извлекаются массивы Numpy
        и помещаются в словарь data под соответствующими именами.
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
        names = ['t', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5'][:self.ch_num + 1]

        if self.recorder_device == 'GTLab D401':
            df = pd.read_csv(file, index_col=False, names=names, sep='\t')
            for num, name in enumerate(names):
                data[name] = df[name].values
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])
            # FIXME Сделать адекватную нормализацию
            # func = sp.interpolate.interp1d(t, ch)
            for i in range(len(data['t']) - 1):
                data['t'][i + 1] = data['t'] + t_step

        elif self.recorder_device == 'WinПОС':
            df = pd.read_csv(file, index_col=False, names=names, sep='\\s+')
            for num, name in enumerate(names):
                data[name] = df[name].values
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])
            # !!! TODO Проверить необходимость добавления фиксированного шага

        elif self.recorder_device == 'Micsig tBook':
            usecols = [3, 4, 10][:self.ch_num + 1]
            df = pd.read_csv(file, index_col=False, names=names,
                             skiprows=13, usecols=usecols)
            for num, name in enumerate(names):
                data[name] = df[name].values
            delay = np.loadtxt(file, delimiter=',', dtype='str',
                               skiprows=5, max_rows=1, usecols=1)
            delay = float(np.ndarray.item(delay).split(' ')[0])
            data['t'] = data['t'] - ((data['t'][-1] - data['t'][0])/2 - delay)
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])

        elif self.recorder_device == 'Rigol DS1000Z Series':
            params_position = slice(self.ch_num + 1, None)
            params = list(map(float,
                              file.readline().split(',')[params_position]))
            t_start, t_step = params[0], params[1]
            df = pd.read_csv(file, index_col=False, names=names)
            for num, name in enumerate(names):
                data[name] = df[name].values
            data['t'] = t_start + t_step*data['t']

        elif self.recorder_device == 'Rigol DS1102E':
            df = pd.read_csv(file, index_col=False, names=names,
                             delimiter=',', skiprows=1)
            for num, name in enumerate(names):
                data[name] = df[name].values
            t_step = (data['t'][-1] - data['t'][0])/len(data['t'])

        elif self.recorder_device == 'Rigol DG4202':
            params_position = slice(self.ch_num + 1, None)
            params = file.readline().split('\t')[params_position]
            params = [float(i.replace(',', '.')) for i in params]
            t_start, t_step = params[0], params[1]
            df = pd.read_csv(file, index_col=False, names=names,
                             delimiter='\t', decimal=',')
            for num, name in enumerate(names):
                data[name] = df[name].values
            data['t'] = t_start + t_step*data['t'].values

        elif self.recorder_device == 'Tektronix MSO46':
            df = pd.read_csv(file, index_col=False, names=names, skiprows=12)
            for num, name in enumerate(names):
                data[name] = df[name].values
        # Работает, если перебор по ключам идет в порядке добавления
        data = np.array([data[key] for key in data.keys()])
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
