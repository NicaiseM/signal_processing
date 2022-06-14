#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library

# Third-party Libraries
import streamlit as st

# Own sources
from processor import Processor

# === Классы ===

# === Функции ===

# === Обработка ===
processor = Processor()

st.title('Signal Processing App')

st.sidebar.title("Настройки")
st.sidebar.info('Выберите необходимые параметры обработки.')
defaultButton = st.sidebar.button('Настройки по умолчанию')
file = st.sidebar.file_uploader('Обрабатываемый csv-файл',
                                help='Поместите файл в эту область')
# file = 'test_working_dir/rigol-new/csv/NewFile3.csv'




timeShiftBox = st.sidebar.checkbox('Ликвидация смещения нуля по времени')
channelShiftBox = st.sidebar.checkbox('Ликвидация смещения нуля сигнала')
timeLimitationBox = st.sidebar.checkbox('Ограничение по времени')
smoothingBox = st.sidebar.checkbox('Сглаживание скользящей средней')





# processor.file_processing(file)
# data = processor.data
# plt.plot(data[0], data[1], data[0], data[2])
