#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library

# Third-party Libraries
import streamlit as st
from numpy import nan

# Own sources
from controller import controller
from metric import metric as mt
import config


# === Классы ===

class UI():
    def __init__(self):
        st.set_page_config(page_title='Signal Processing App')
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
                width: 400px;
            }
            [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
                width: 400px;
                margin-left: -400px;
            }
            """,
            unsafe_allow_html=True,
        )
        st.title('Signal Processing App')
        self.sidebar_init()
        st.pyplot(controller.processor.plotter.fig)
        # !!! Для проверки частоты обновления скрипта streamlit
        st.write(controller.counter)
        controller.counter += 1

    def sidebar_init(self):
        st.sidebar.title("Настройки")

        defaultButton = st.sidebar.button('Настройки по умолчанию')
        if defaultButton:
            controller.cfg_to_default_reset()

        self.file = st.sidebar.file_uploader(
            'Обрабатываемый csv-файл',
            help='Поместите файл в эту область'
            )

        self.time_shift_removal()
        self.channel_shift_removal()
        self.time_limitation()
        self.moving_average_smoothing()
        self.metric_factors()

        startButton = st.sidebar.button('Запуск обработки')
        if startButton:
            controller.processing_start(self.file)
        # self.__debug()

    def time_shift_removal(self):
        self.timeShiftBox = st.sidebar.checkbox(
            'Ликвидация смещения нуля времени'
            )
        self.change_cfg('time_shift', self.timeShiftBox)

    def channel_shift_removal(self):
        self.channelShiftBox = st.sidebar.checkbox(
            'Ликвидация смещения нуля сигнала'
            )
        self.change_cfg('channel_shift', self.channelShiftBox)

        if self.channelShiftBox:
            min_n, max_n = 0, 500
            self.ch_shift_amount = st.sidebar.slider(
                'Число первых выборок для определения нуля',
                min_value=min_n,
                max_value=max_n,
                value=int(1/2*(max_n - min_n))
                )
            self.change_cfg('ch_shift_amount', self.ch_shift_amount)

    def time_limitation(self):
        self.timeLimitationBox = st.sidebar.checkbox(
            'Ограничение по времени'
            )
        self.change_cfg('time_shift', self.timeLimitationBox)

        if self.timeLimitationBox:
            self.time_limits = []
            st.sidebar.text('Левая граница по времени')
            col1, col2 = st.sidebar.columns(2)
            with col1:
                self.base_left = st.number_input(
                        'Мантисса слева',
                        value=0,
                        step=1
                        )
            with col2:
                self.power_left = st.number_input(
                    'Показатель слева',
                    value=0,
                    step=1
                    )
            self.time_limits.append(self.base_left*10**self.power_left)

            st.sidebar.text('Правая граница по времени')
            col3, col4 = st.sidebar.columns(2)
            with col3:
                self.base_right = st.number_input(
                        'Мантисса справа',
                        value=1,
                        step=1
                        )
            with col4:
                self.power_right = st.number_input(
                    'Показатель справа',
                    value=1000,
                    step=1
                    )
            self.time_limits.append(self.base_right*10**self.power_right)

            self.change_cfg('time_limits', self.time_limits)
            st.write(config.configurator.cfg['devices']['Rigol DS1000Z Series']['processing']['time_limits'])

    def moving_average_smoothing(self):
        self.smoothingBox = st.sidebar.checkbox(
            'Сглаживание скользящей средней'
            )
        self.change_cfg('moving_average_smoothing', self.smoothingBox)

        if self.smoothingBox:
            min_n, max_n = 0, 100
            self.smooth_window = st.sidebar.slider(
                'Ширина окна сглаживания',
                min_value=min_n,
                max_value=max_n,
                value=int(1/2*(max_n - min_n))
                )
            self.change_cfg('moving_average_window', self.smooth_window)

    def metric_factors(self):
        self.t_mt_factor = st.sidebar.select_slider(
            'Метрический коэффициент t',
            mt.keys(),
            value=0
            )
        self.change_cfg('t_mt_factor', self.t_mt_factor)

        self.ch1_mt_factor = st.sidebar.select_slider(
            'Метрический коэффициент сигнала №1',
            mt.keys(),
            value=0,
            )
        self.change_cfg('ch1_mt_factor', self.ch1_mt_factor)

        self.ch2_mt_factor = st.sidebar.select_slider(
            'Метрический коэффициент ch2',
            mt.keys(),
            value=0,
            )
        self.change_cfg('ch2_mt_factor', self.ch2_mt_factor)

    def change_cfg(self, key, value):
        controller.cfg_update(key, value)

    def __debug(self):
        debugButton = st.sidebar.button('Отладка')
        if debugButton:
            st.write('In st', self.t_mt_factor)
            st.write(controller.processor.device)
            st.write('In cfg',
                      config.configurator.cfg['metric']['t_mt_factor'])


# === Функции ===

# === Обработка ===

ui = UI()
