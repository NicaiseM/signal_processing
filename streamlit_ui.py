#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library

# Third-party Libraries
import streamlit as st
from numpy import nan

# Own sources
from controller import Controller


# === Классы ===

# === Функции ===

# === Обработка ===
controller = Controller()

st.title('Signal Processing App')

st.sidebar.title("Настройки")
st.sidebar.info('Выберите необходимые параметры обработки.')
defaultButton = st.sidebar.button('Настройки по умолчанию')
if defaultButton:
    controller.processor.cfg_to_default_reset()
file = st.sidebar.file_uploader('Обрабатываемый csv-файл',
                                help='Поместите файл в эту область')
# file = 'test_working_dir/rigol-new/csv/NewFile3.csv'

timeShiftBox = st.sidebar.checkbox('Ликвидация смещения нуля по времени')
channelShiftBox = st.sidebar.checkbox('Ликвидация смещения нуля сигнала')
if channelShiftBox:
    txt = 'Число первых выборок для определения нуля'
    min_n, max_n = 0, 5000
    ch_shift_amount = st.sidebar.slider(txt, min_value=min_n, max_value=max_n,
                                        value=[min_n, max_n])  # Два значения в слайдере!
else:
    ch_shift_amount = 0
timeLimitationBox = st.sidebar.checkbox('Ограничение по времени')
if timeLimitationBox:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        t_left = st.number_input('Левая граница по времени')
    with col2:
        t_right = st.number_input('Правая граница по времени')
else:
    t_left, t_right = nan, nan
smoothingBox = st.sidebar.checkbox('Сглаживание скользящей средней')
if smoothingBox:
    txt = 'Ширина окна сглаживания'
    min_n, max_n = 0, 5000
    smooth_window = st.sidebar.slider(txt, min_value=min_n, max_value=max_n,
                                      value=[min_n, max_n])
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
    controller.processing_start(cfg, file)  # .getvalue() не работает


# processor.file_processing(file)
# data = processor.data
# plt.plot(data[0], data[1], data[0], data[2])
