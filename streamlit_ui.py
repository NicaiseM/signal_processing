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
import configurator


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
        st.write(st.session_state)

    def sidebar_init(self):
        st.sidebar.header("Настройки")

        self.file = st.sidebar.file_uploader(
            'Обрабатываемый csv-файл',
            help='Поместите файл в эту область'
            )

        self.buttons()
        self.current_settings_set()

        if controller.last_file:
            self.optionsContainer = st.sidebar.container()
            with self.optionsContainer:
                self.inverting()
                self.time_shift_removal()
                self.channel_shift_removal()
                self.time_limitation()
                self.moving_average_smoothing()
                self.metric_factors()

    def buttons(self):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            defaultButton = st.button(
                'По умолчанию'
                )
            if defaultButton:
                controller.cfg_to_default_reset()
                st.session_state.clear()
                if controller.last_file:
                    controller.processing_start(controller.last_file)
        with col2:
            startButton = st.button(
                'Запуск обработки'
                )
            if startButton:
                controller.processing_start(self.file)

    def current_settings_set(self):
        if controller.last_file:
            device = controller.processor.device
            prc_cfg = configurator.configurator.cfg['devices']
            prc_cfg = prc_cfg[device]['processing']
            mt_cfg = configurator.configurator.cfg['metric']
            self.cfg = {
                'invert': prc_cfg['invert'],
                'timeShiftBox': prc_cfg['time_shift'],
                'channelShiftBox': prc_cfg['channel_shift'],
                'ch_shift_min': 0,
                'ch_shift_max': 500,
                'ch_shift_amount': prc_cfg['channel_shift_amount'],
                'timeLimitationBox': prc_cfg['time_limitation'],
                'time_limits': prc_cfg['time_limits'],
                'smoothingBox': prc_cfg['moving_average_smoothing'],
                'smooth_window_min': 0,
                'smooth_window_max': 100,
                'smooth_window': prc_cfg['moving_average_window'],
                't_mt_factor': mt_cfg['t_mt_factor'],
                'ch1_mt_factor': mt_cfg['ch1_mt_factor'],
                'ch2_mt_factor': mt_cfg['ch2_mt_factor']
                }
            for key, value in self.cfg.items():
                if key not in st.session_state:
                    st.session_state[key] = value
                    if key == 'invert':
                        st.session_state['invert_mask'] =\
                            self.invert_list_converting(value, 'to_str')

    def invert_list_converting(self, input_list, type_to):
        length = len(st.session_state['invert'])
        st.session_state['ch_names'] = ['Ch' + str(i + 1) for i in range(length)]
        if type_to == 'to_str':
            return [i for i, j in zip(st.session_state['ch_names'],
                                      input_list) if j]
        elif type_to == 'to_bool':
            return [i in input_list for i in st.session_state['ch_names']]
        else:
            raise TypeError

    def inverting(self):
        self.invert_mask = st.multiselect(
            'Инверсия каналов',
            options=st.session_state['ch_names'],
            key='invert_mask'
            )
        self.invert = self.invert_list_converting(self.invert_mask, 'to_bool')
        self.change_cfg('invert', self.invert)

    def time_shift_removal(self):
        self.timeShiftBox = st.checkbox(
            'Ликвидация смещения нуля времени',
            key='timeShiftBox'
            )
        self.change_cfg('time_shift', self.timeShiftBox)

    def channel_shift_removal(self):
        self.channelShiftBox = st.checkbox(
            'Ликвидация смещения нуля сигнала',
            key='channelShiftBox'
            )
        self.change_cfg('channel_shift', self.channelShiftBox)

        if self.channelShiftBox:
            self.ch_shift_amount = st.slider(
                'Число первых выборок для определения нуля',
                min_value=st.session_state['ch_shift_min'],
                max_value=st.session_state['ch_shift_max'],
                key='ch_shift_amount'
                )
            self.change_cfg('ch_shift_amount', self.ch_shift_amount)

    def time_limitation(self):
        self.timeLimitationBox = st.checkbox(
            'Ограничение по времени',
            key='timeLimitationBox'
            )
        self.change_cfg('time_limitation', self.timeLimitationBox)

        if self.timeLimitationBox:
            self.time_limits = self.cfg['time_limits']  # !!!
            st.sidebar.write('Левая граница по времени')
            col1, col2 = st.columns(2)
            with col1:
                self.base_left = st.number_input(
                    'Мантисса слева',
                    value=-10000,
                    step=1
                    )
            with col2:
                self.power_left = st.number_input(
                    'Показатель слева',
                    value=0,
                    step=1
                    )
            self.time_limits[0] = self.base_left*10**self.power_left

            st.sidebar.write('Правая граница по времени')
            col3, col4 = st.columns(2)
            with col3:
                self.base_right = st.number_input(
                    'Мантисса справа',
                    value=10000,
                    step=1
                    )
            with col4:
                self.power_right = st.number_input(
                    'Показатель справа',
                    value=0,
                    step=1
                    )
            self.time_limits[1] = self.base_right*10**self.power_right

            st.session_state['time_limits'] = self.time_limits
            self.change_cfg('time_limits', self.time_limits)

    def moving_average_smoothing(self):
        self.smoothingBox = st.checkbox(
            'Сглаживание скользящей средней',
            key='smoothingBox'
            )
        self.change_cfg('moving_average_smoothing', self.smoothingBox)

        if self.smoothingBox:
            self.smooth_window = st.slider(
                'Ширина окна сглаживания',
                min_value=st.session_state['smooth_window_min'],
                max_value=st.session_state['smooth_window_max'],
                key='smooth_window'
                )
            self.change_cfg('moving_average_window', self.smooth_window)

    def metric_factors(self):
        self.t_mt_factor = st.select_slider(
            'Метрический коэффициент t',
            mt.keys(),
            key='t_mt_factor'
            )
        self.change_cfg('t_mt_factor', self.t_mt_factor)

        self.ch1_mt_factor = st.select_slider(
            'Метрический коэффициент сигнала №1',
            mt.keys(),
            key='ch1_mt_factor',
            )
        self.change_cfg('ch1_mt_factor', self.ch1_mt_factor)

        self.ch2_mt_factor = st.select_slider(
            'Метрический коэффициент ch2',
            mt.keys(),
            key='ch2_mt_factor',
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
                     configurator.configurator.cfg['metric']['t_mt_factor'])


# === Функции ===

# === Обработка ===

ui = UI()
