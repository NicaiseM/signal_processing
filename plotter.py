#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library

# Third-party Libraries
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Own sources
import config

# === Классы ===

class Plotter():
    def __init__(self, canvas=None):
        self.cfg = config.configurator.cfg['visualization']
        plt.ioff()
        self.canvas = canvas
        if canvas is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig = canvas.fig
            self.ax = canvas.ax
        self.logo(self.ax)

    def logo(self, ax):
        logo_x = np.linspace(0, np.pi*2)
        logo_y = np.sin(logo_x)
        ax.plot(logo_x, logo_y)

    def plotting(self, t, ch1, ch2=None,
                 t_mt_factor=1, ch1_mt_factor=1, ch2_mt_factor=1,
                 ch1_label='u(t)', ch2_label='i(t)',
                 t_xlabel='t, {}с',
                 ch1_ylabel='u(t), {}В',
                 ch2_ylabel='i(t), {}А',
                 ):
        self.ax.cla()
        self.ax.plot(t/t_mt_factor[0], ch1/ch1_mt_factor[0],
                     'C0-', label=ch1_label)
        if ch2 is not None:
            self.ax.plot(t/t_mt_factor[0], ch2/ch2_mt_factor[0],
                         'C1-', label=ch2_label)
            ch2_ylabel = '; ' + ch2_ylabel
        else:
            ch2_ylabel = ''
        self.ax.grid(True)
        self.ax.set_xlabel(t_xlabel.format(t_mt_factor[1]))
        self.ax.set_ylabel(ch1_ylabel.format(ch1_mt_factor[1])
                           + ch2_ylabel.format(ch2_mt_factor[1]))
        self.fig.tight_layout()
        if self.cfg['show_title']:
            self.ax.set_title('Осциллограмма напряжения и тока')
        if self.cfg['show_legend']:
            self.ax.legend(loc='best')
        if self.canvas is None:
            if mpl.get_backend() == 'Qt5Agg':
                self.fig.show()
            else:
                pass
        else:
            self.canvas.draw()

# === Функции ===

# === Обработка ===
