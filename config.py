#!/usr/bin/env python
# -*- coding: utf-8 -*-

cfg = {
    'devices': {
        'Globaltest': {  # FIXME Правильное название и сигнатура
            'signature_1ch': 'FIXME',  # FIXME Заполнить
            'signature_2ch': 'time\t',
            'position': (0, 5),
            'invert': [True, True]
        },
        'Gydropribor': {  # FIXME Правильное название и сигнатура
            'signature_1ch': '   ',
            'signature_2ch': 'FIXME',  # FIXME Заполнить
            'position': (0, 4),
            'invert': [False, False]
        },
        'Micsig tBook': {
            'signature_1ch': 'ProID,Info,,time,Vo',
            'signature_2ch': ('ProID,Info,Unnamed: 2,time,Vol.,Unnamed: 5,'
                              + 'ProID,Info,Unnamed: 2,time,Vol.,Unnamed'),
            'position': (0, -4),
            'invert': [False, False]
        },
        'Rigol MSO1104Z/DS1074Z': {
            'signature_1ch': 'X,CH1,Start,Increment',
            'signature_2ch': 'X,CH1,CH2,Start,Increment',
            'position': (0, -2),
            'invert': [False, False]
        },
        'Rigol DS1102E': {
            'signature_1ch': 'Time,X(CH1)',
            'signature_2ch': 'Time,X(CH1),X(CH2)',  # !!! Снять
            'position': (0, -2),
            'invert': [False, False]
        },
        'Rigol (unknown)': {  # FIXME Что это за прибор? Узнать!
            'signature_1ch': 'X\tCH1\tStart\tIncrement',
            'signature_2ch': 'X\tCH1\tCH2\tStart\tIncrement',  # !!! Снять
            'position': (0, -2),
            'invert': [False, False]
        },
        'Tektronix MSO46': {
            'signature_1ch': 'X,CH1,Start,Increment',  # !!! Снять
            'signature_2ch': 'X,CH1,CH2,Start,Increment',
            'position': (0, -1),
            'invert': [True, True]
        }
        # TODO 'Tektronix TDS1012B', 'Tektronix TDS2012C'
    }
}
