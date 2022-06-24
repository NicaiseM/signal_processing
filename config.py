#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Сбор конфигурации из файлов в один модуль."""

# Future
# from __future__ import

# Standard Library

# Third-party Libraries

# Own sources
import yaml


# === Классы ===
class Configurator():
    """Класс формирования конфигурации."""

    def __init__(self):
        """
        Инициализация конфигуратора.

        Returns
        -------
        None.

        Notes
        -----
        Yaml-файл конфигурации открывается, его содержимое заносится
        в словарь конфигурации по умолчанию, после чего организуется
        неглубокая копия данного словаря, которая в дальнейшем будет
        изменяться в ходе выполнения программы и смены настроек.

        """
        with open('./config_default.yml', 'r', encoding='utf-8') as f:
            self.default_cfg = yaml.safe_load(f)
            self.cfg = self.default_cfg.copy()

    def cfg_to_default_reset(self):
        """
        Возвращение конфигуратора к настройкам по умолчанию.

        Returns
        -------
        None.

        Notes
        -----
        В поле текущих настроек перезаписываются изначальные параметры.

        """
        self.cfg = self.default_cfg.copy()

    def device_cfg_extract(self, category, device=None):
        """
        Выделение настроек заданных категории и (возможно) прибора

        Parameters
        ----------
        category : str
            Выделяемая категория настроек.
        device : str, optional
            Название прибора. The default is None.

        Returns
        -------
        tmp_cfg : dict
            Словарь выделенных настроек.

        Notes
        -----
        Если задан прибор, для которого выделяются настройки из словаря
        общей конфигурации программы, то во временную переменную tmp_cfg
        размещаются ссылки на параметры заданной категории определенного
        прибора, иначе в этой переменной размещаются ссылки на параметры
        заданной категории для всех приборов с сохранением иерархии
        прибор/категория. Временная переменная возвращается, и может
        быть присвоена полю другого класса, для которого и производилось
        выделение настроек.
        NB: В словаре выделенных настроек будут размещены не копии
        элементов исходного словаря, а указатели на них, поэтому
        изменение параметров в ходе работы с той переменной, которой
        присваивается результат работы данного метода, будет отражаться
        на состоянии общего словаря настроек - self.cfg.

        """
        if device is not None:
            tmp_cfg = self.cfg['devices'][device][category]
        else:
            tmp_cfg = {}
            for device in self.cfg['devices']:
                tmp_cfg[device] = self.cfg['devices'][device][category]
        return tmp_cfg

    def cfg_update(self, key, value, device=None):
        if key in self.cfg['metric']:
            self.cfg['metric'][key] = value
        elif device is not None:
            if key in self.cfg['devices'][device]['processing']:
                self.cfg['devices'][device]['processing'][key] = value


# === Функции ===

# === Обработка ===
configurator = Configurator()
