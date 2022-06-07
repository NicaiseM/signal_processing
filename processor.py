#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Future
# from __future__ import

# Standard Library
import os
import time
from pathlib import Path

# Third-party Libraries
import scipy
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Own sources
from opener import Opener
from metric import metric as mt
from service_utilities import TimeTest


class Processor():
    def __init__(self):
        self.opener = Opener()
    def file_processing(self, file):
        device, data, t_step = self.opener.read(file)


