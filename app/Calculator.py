# -*- coding: utf-8 -*-

# @autor: Sebastian Rohner
# @github: github.com/Syncriix

# Builtins
import sys 
import os
import platform

import tkinter as tk
from tkinter import Menu, FALSE

from functools import partial
from json import load as json_load
from json import dump as json_dump

from copy import deepcopy

# Local
from .calc import Calc


class Calculator(object):
    """Klasse für die Erstellung des Layouts des Rechners, 
    die Verteilung der Schaltflächen und die Einrichtung seiner Funktionalitäten.

    Die im Layout verteilten Schaltflächen sind wie im folgenden Beispiel dargestellt:

        C | ( | ) | <
        7 | 8 | 9 | x
        4 | 5 | 6 | -
        1 | 2 | 3 | +
        . | 0 | = | /
          |   | ^ | √

        HINWEIS: Es ist notwendig, das im View-Paket enthaltene Style-Modul zu importieren, 
        zu importieren und eine seiner Style-Klassen auszuwählen.
    """

    def __init__(self, master):
        self.master = master
        self.calc = Calc()



    def _exit(self):
        exit()
