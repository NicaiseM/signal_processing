#!/usr/bin/env python
# -*- coding: utf-8 -*-

class WrongCsvStructureError(Exception):
    """Исключение неверного формата данных в csv-файле."""

    def __init__(self, *file):
        if file:
            file = str(file[0])
            self.message = f'File {file} has invalid structure.'
        else:
            self.message = 'Invalid csv-file structure.'

    def __str__(self):
        return(f'WrongCsvStructureError: {self.message}')
