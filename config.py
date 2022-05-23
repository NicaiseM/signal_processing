#!/usr/bin/env python
# -*- coding: utf-8 -*-

cfg = {
'devices': {
    'globaltest': {
        'signature': 'time\t',
        'position': (0, 5)
        },
    'gydropribor': {
        'signature': '   ',
        'position': (0, 4)
        },
    'micsig1ch': {
        'signature': 'ProID,Info,,time,Vol.',
        'position': (0, -2)
        },
    'micsig2ch': {
        'signature': ('ProID,Info,Unnamed: 2,time,Vol.,Unnamed: 5,'
                      + 'ProID,Info,Unnamed: 2,time,Vol.,Unnamed: '),
        'position': (0, -2)
        },
    'rigol-new': {
        'signature': 'X,CH1,CH2,Start,Increment',
        'position': (0, -2)
        },
    'rigol-old': {
        'signature': 'Time,X(CH1),X(CH2)',
        'position': (0, -2)
        },
    'tektronix': {
        'signature': 'X,CH1,CH2,Start,Increment',
        'position': (0, -1)
        },
    }
}
