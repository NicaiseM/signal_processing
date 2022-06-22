#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library
from io import StringIO

# Third-party Libraries
import streamlit as st
import matplotlib.pyplot as plt
from numpy import nan

# Own sources
from controller import Controller


# === Классы ===

# === Функции ===

# === Обработка ===
controller = Controller()

st.title('Signal Processing App')

# Настройки программы
st.sidebar.title("Настройки")
st.sidebar.info('Выберите необходимые параметры обработки.')

# Возвращение к настройкам по умолчанию
defaultButton = st.sidebar.button('Настройки по умолчанию')
if defaultButton:
    controller.processor.cfg_to_default_reset()

# Открытие файла
file = st.sidebar.file_uploader('Обрабатываемый csv-файл',
                                help='Поместите файл в эту область')

uploaded_file = st.sidebar.file_uploader("Add text file !")
if uploaded_file:
    line = uploaded_file.readline()
    print(line)
    st.write(line)

# Ликвидация смещения нуля
timeShiftBox = st.sidebar.checkbox('Ликвидация смещения нуля по времени')
channelShiftBox = st.sidebar.checkbox('Ликвидация смещения нуля сигнала')
if channelShiftBox:
    txt = 'Число первых выборок для определения нуля'
    min_n, max_n = 0, 5000
    ch_shift_amount = st.sidebar.slider(txt, min_value=min_n, max_value=max_n,
                                        value=1/2*(max_n - min_n))
else:
    ch_shift_amount = 0

# Ограничение по времени
timeLimitationBox = st.sidebar.checkbox('Ограничение по времени')
if timeLimitationBox:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        t_left = st.number_input('Левая граница по времени')
    with col2:
        t_right = st.number_input('Правая граница по времени')
else:
    t_left, t_right = nan, nan

# Сглаживание скользящей средней
smoothingBox = st.sidebar.checkbox('Сглаживание скользящей средней')
if smoothingBox:
    txt = 'Ширина окна сглаживания'
    min_n, max_n = 0, 5000
    smooth_window = st.sidebar.slider(txt, min_value=min_n, max_value=max_n,
                                      value=1/2*(max_n - min_n))
else:
    smooth_window = 0

cfg = {
    'time_shift': timeShiftBox,
    'channel_shift': channelShiftBox,
    'channel_shift_amount': ch_shift_amount,
    'time_limitation': timeLimitationBox,
    'time_limits': [t_left, t_right],
    'moving_average_smoothing': smoothingBox,
    'moving_average_window': smooth_window
}

startButton = st.sidebar.button('Запуск обработки')
if startButton:
    controller.processing_start(file)  # .getvalue() не работает
    data = controller.processor.data
    plt.plot(data[0], data[1], data[0], data[2])


# processor.file_processing(file)
# data = processor.data
# plt.plot(data[0], data[1], data[0], data[2])
