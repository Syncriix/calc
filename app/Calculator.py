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

        self.settings = self._load_settings()

        # Legt den Standardstil für macOS fest, wenn es als Betriebssystem verwendet wird
        if platform.system() == 'Darwin':
            self.theme = self._get_theme('Default Theme For MacOS')
        else:
            self.theme = self._get_theme(self.settings['current_theme'])

        # Top-Level-Ausgabe
        self.master.title('Malia Calculator')
        self.master.minsize(width=680, height=415)
        self.master.geometry('-150+100')
        self.master.resizable(True, True)
        self.master['bg'] = self.theme['master_bg']

        # Eingabebereich
        self._frame_input = tk.Frame(self.master, bg=self.theme['frame_bg'])
        self._frame_input.pack(padx=20)
        self._frame_input.rowconfigure(0, weight=1)
        self._frame_input.columnconfigure(0, weight=1)

        # Bereich der Schaltfläche
        self._frame_buttons = tk.Frame(self.master, bg=self.theme['frame_bg'])
        self._frame_buttons.pack(
            side="top", padx=20, pady=20, fill=tk.BOTH, expand=True)
        self._frame_buttons.rowconfigure(tuple(range(6)), weight=1)
        self._frame_buttons.columnconfigure(tuple(range(8)), weight=1)

        # Start-up-Funktionen
        self._create_input(self._frame_input)
        self._create_buttons(self._frame_buttons)
        self._create_menu(self.master)

    @staticmethod
    def _load_settings():
        """Dienstprogramm zum Laden der Rechner-Konfigurationsdatei."""
        with open('./app/settings/settings.json', mode='r', encoding='utf-8') as f:
            settings = json_load(f)

        return settings

    def _get_theme(self, name='Dark'):
        """Gibt die Stileinstellungen für das angegebene Thema zurück."""

        list_of_themes = self.settings['themes']

        found_theme = None
        for t in list_of_themes:
            if name == t['name']:
                found_theme = deepcopy(t)
                break

        return found_theme

    def _create_input(self, master):
        self._entry = tk.Entry(master, cnf=self.theme['INPUT'])
        self._entry.insert(0, 0)
        self._entry.pack(ipadx=20, fill=tk.X, expand=True)

    def _create_menu(self, master):
        self.master.option_add('*tearOff', FALSE)
        calc_menu = Menu(self.master)
        self.master.config(menu=calc_menu)

        # Konfiguration
        config = Menu(calc_menu)
        theme = Menu(config)
        # Themen Menu
        incompitables_theme = ['Default Theme For MacOS']
        for t in self.settings['themes']:

            name = t['name']
            if name in incompitables_theme:  # Nicht kompatible Themen ignorieren.
                continue
            else:
                theme.add_command(label=name, command=partial(
                    self._change_theme_to, name))
        # Konfiguration
        calc_menu.add_cascade(label='Konfiguration', menu=config)
        config.add_cascade(label='Theme', menu=theme)

        config.add_separator()
        config.add_command(label='Beenden', command=self._exit)

    def _change_theme_to(self, name='Dark'):
        self.settings['current_theme'] = name

        with open('./app/settings/settings.json', 'w') as outfile:
            json_dump(self.settings, outfile, indent=4)

        self._realod_app()

    def _create_buttons(self, master):
        """"Methode, die für die Erstellung aller Schaltflächen des Taschenrechners verantwortlich ist,
        vom Hinzufügen von Ereignissen zu den einzelnen Schaltflächen bis hin zu ihrer Verteilung auf dem Rasterlayout.
        """

        # Globale Einstellungen (Breite, Höhe, Schriftart usw.) für die angegebene Schaltfläche festlegen.
        self.theme['BTN_NUMBER'].update(self.settings['global'])

        self._BTN_NUM_0 = tk.Button(
            master, text=0, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_1 = tk.Button(
            master, text=1, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_2 = tk.Button(
            master, text=2, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_3 = tk.Button(
            master, text=3, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_4 = tk.Button(
            master, text=4, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_5 = tk.Button(
            master, text=5, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_6 = tk.Button(
            master, text=6, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_7 = tk.Button(
            master, text=7, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_8 = tk.Button(
            master, text=8, cnf=self.theme['BTN_NUMBER'])
        self._BTN_NUM_9 = tk.Button(
            master, text=9, cnf=self.theme['BTN_NUMBER'])

        # Globale Einstellungen (Breite, Höhe, Schriftart usw.) für die angegebene Schaltfläche festlegen.
        self.theme['BTN_OPERATOR'].update(self.settings['global'])

        # Instanziierung der Schaltflächen der numerischen Operatoren
        self._BTN_ADD = tk.Button(
            master, text='+', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_SUB = tk.Button(
            master, text='-', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_DIV = tk.Button(
            master, text='/', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_MULT = tk.Button(
            master, text='*', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_EXP = tk.Button(
            master, text='^', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_SQR = tk.Button(
            master, text='√', cnf=self.theme['BTN_OPERATOR'])

        # Globale Einstellungen (Breite, Höhe, Schriftart usw.) für die angegebene Schaltfläche festlegen.
        self.theme['BTN_DEFAULT'].update(self.settings['global'])
        self.theme['BTN_CLEAR'].update(self.settings['global'])

        # Installation der Funktionstasten des Rechners.
        self._BTN_OPEN_PARENT = tk.Button(
            master, text='(', cnf=self.theme['BTN_DEFAULT'])
        self._BTN_CLOSE_PARENT = tk.Button(
            master, text=')', cnf=self.theme['BTN_DEFAULT'])
        self._BTN_CLEAR = tk.Button(
            master, text='C', cnf=self.theme['BTN_DEFAULT'])
        self._BTN_DEL = tk.Button(
            master, text='<', cnf=self.theme['BTN_CLEAR'])
        self._BTN_RESULT = tk.Button(
            master, text='=', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_DOT = tk.Button(
            master, text='.', cnf=self.theme['BTN_DEFAULT'])

        # Installation der Wissenschaftlichen Funktionstasten des Rechners.
        self._BTN_PI = tk.Button(
            master, text='π', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_SIN = tk.Button(
            master, text='sin', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_COS = tk.Button(
            master, text='cos', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_TAN = tk.Button(
            master, text='tan', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_2PI = tk.Button(
            master, text='2π', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_COSH = tk.Button(
            master, text='cosh', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_TANH = tk.Button(
            master, text='tanh', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_SINH = tk.Button(
            master, text='sinh', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_LOG = tk.Button(
            master, text='log', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_INV = tk.Button(
            master, text='inv', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_MOD = tk.Button(
            master, text='mod', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_E = tk.Button(
            master, text='e', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_LOG2 = tk.Button(
            master, text='log2', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_DEG = tk.Button(
            master, text='deg', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_ACOSH = tk.Button(
            master, text='acosh', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_ASINH = tk.Button(
            master, text='asinh', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_LOG10 = tk.Button(
            master, text='log10', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_LOG1P = tk.Button(
            master, text='log1p', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_EXPM1 = tk.Button(
            master, text='expm1', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_LGAMMA = tk.Button(
            master, text='lgamma', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_RAD = tk.Button(
            master, text='rad', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_GAMMA = tk.Button(
            master, text='gamma', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_ERF = tk.Button(
            master, text='erf', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_ERFC = tk.Button(
            master, text='erfc', cnf=self.theme['BTN_OPERATOR'])

        # Instanziierung der leeren Schaltflächen, für die zukünftige Implementierung
        self._BTN_EMPTY1 = tk.Button(
            master, text='', cnf=self.theme['BTN_OPERATOR'])
        self._BTN_EMPTY2 = tk.Button(
            master, text='', cnf=self.theme['BTN_OPERATOR'])

        # Verteilung von Schaltflächen in einem Grid-Layout-Manager
        # Zeile 0
        self._BTN_CLEAR.grid(row=0, column=0, padx=1, pady=1, sticky="news")
        self._BTN_OPEN_PARENT.grid(
            row=0, column=1, padx=1, pady=1, sticky="news")
        self._BTN_CLOSE_PARENT.grid(
            row=0, column=2, padx=1, pady=1, sticky="news")
        self._BTN_DEL.grid(row=0, column=3, padx=1, pady=1, sticky="news")
        self._BTN_PI.grid(row=0, column=4, padx=1, pady=1, sticky="news")
        self._BTN_SIN.grid(row=0, column=5, padx=1, pady=1, sticky="news")
        self._BTN_COS.grid(row=0, column=6, padx=1, pady=1, sticky="news")
        self._BTN_TAN.grid(row=0, column=7, padx=1, pady=1, sticky="news")

        # Zeile 1
        self._BTN_NUM_7.grid(row=1, column=0, padx=1, pady=1, sticky="news")
        self._BTN_NUM_8.grid(row=1, column=1, padx=1, pady=1, sticky="news")
        self._BTN_NUM_9.grid(row=1, column=2, padx=1, pady=1, sticky="news")
        self._BTN_MULT.grid(row=1, column=3, padx=1, pady=1, sticky="news")
        self._BTN_2PI.grid(row=1, column=4, padx=1, pady=1, sticky="news")
        self._BTN_COSH.grid(row=1, column=5, padx=1, pady=1, sticky="news")
        self._BTN_TANH.grid(row=1, column=6, padx=1, pady=1, sticky="news")
        self._BTN_SINH.grid(row=1, column=7, padx=1, pady=1, sticky="news")

        # Zeile 2
        self._BTN_NUM_4.grid(row=2, column=0, padx=1, pady=1, sticky="news")
        self._BTN_NUM_5.grid(row=2, column=1, padx=1, pady=1, sticky="news")
        self._BTN_NUM_6.grid(row=2, column=2, padx=1, pady=1, sticky="news")
        self._BTN_SUB.grid(row=2, column=3, padx=1, pady=1, sticky="news")
        self._BTN_LOG.grid(row=2, column=4, padx=1, pady=1, sticky="news")
        self._BTN_INV.grid(row=2, column=5, padx=1, pady=1, sticky="news")
        self._BTN_MOD.grid(row=2, column=6, padx=1, pady=1, sticky="news")
        self._BTN_E.grid(row=2, column=7, padx=1, pady=1, sticky="news")

        # Zeile 3
        self._BTN_NUM_1.grid(row=3, column=0, padx=1, pady=1, sticky="news")
        self._BTN_NUM_2.grid(row=3, column=1, padx=1, pady=1, sticky="news")
        self._BTN_NUM_3.grid(row=3, column=2, padx=1, pady=1, sticky="news")
        self._BTN_ADD.grid(row=3, column=3, padx=1, pady=1, sticky="news")
        self._BTN_RAD.grid(row=3, column=4, padx=1, pady=1, sticky="news")
        self._BTN_GAMMA.grid(row=3, column=5, padx=1, pady=1, sticky="news")
        self._BTN_ERF.grid(row=3, column=6, padx=1, pady=1, sticky="news")
        self._BTN_ERFC.grid(row=3, column=7, padx=1, pady=1, sticky="news")

        # Zeile 4
        self._BTN_DOT.grid(row=4, column=0, padx=1, pady=1, sticky="news")
        self._BTN_NUM_0.grid(row=4, column=1, padx=1, pady=1, sticky="news")
        self._BTN_RESULT.grid(row=4, column=2, padx=1, pady=1, sticky="news")
        self._BTN_DIV.grid(row=4, column=3, padx=1, pady=1, sticky="news")
        self._BTN_LOG2.grid(row=4, column=4, padx=1, pady=1, sticky="news")
        self._BTN_DEG.grid(row=4, column=5, padx=1, pady=1, sticky="news")
        self._BTN_ACOSH.grid(row=4, column=6, padx=1, pady=1, sticky="news")
        self._BTN_ASINH.grid(row=4, column=7, padx=1, pady=1, sticky="news")

        # Zeile 5
        self._BTN_EMPTY1.grid(row=5, column=0, padx=1, pady=1, sticky="news")
        self._BTN_EMPTY2.grid(row=5, column=1, padx=1, pady=1, sticky="news")
        self._BTN_EXP.grid(row=5, column=2, padx=1, pady=1, sticky="news")
        self._BTN_SQR.grid(row=5, column=3, padx=1, pady=1, sticky="news")
        self._BTN_LOG10.grid(row=5, column=4, padx=1, pady=1, sticky="news")
        self._BTN_LOG1P.grid(row=5, column=5, padx=1, pady=1, sticky="news")
        self._BTN_EXPM1.grid(row=5, column=6, padx=1, pady=1, sticky="news")
        self._BTN_LGAMMA.grid(row=5, column=7, padx=1, pady=1, sticky="news")

        # Anzahl Schaltflächen Ereignisse
        self._BTN_NUM_0['command'] = partial(self._set_values_in_input, 0)
        self._BTN_NUM_1['command'] = partial(self._set_values_in_input, 1)
        self._BTN_NUM_2['command'] = partial(self._set_values_in_input, 2)
        self._BTN_NUM_3['command'] = partial(self._set_values_in_input, 3)
        self._BTN_NUM_4['command'] = partial(self._set_values_in_input, 4)
        self._BTN_NUM_5['command'] = partial(self._set_values_in_input, 5)
        self._BTN_NUM_6['command'] = partial(self._set_values_in_input, 6)
        self._BTN_NUM_7['command'] = partial(self._set_values_in_input, 7)
        self._BTN_NUM_8['command'] = partial(self._set_values_in_input, 8)
        self._BTN_NUM_9['command'] = partial(self._set_values_in_input, 9)

        # Ereignisse der mathematischen Operationstasten
        self._BTN_ADD['command'] = partial(self._set_operator_in_input, '+')
        self._BTN_SUB['command'] = partial(self._set_operator_in_input, '-')
        self._BTN_MULT['command'] = partial(self._set_operator_in_input, '*')
        self._BTN_DIV['command'] = partial(self._set_operator_in_input, '/')
        self._BTN_EXP['command'] = partial(self._set_operator_in_input, '**')
        self._BTN_SQR['command'] = partial(
            self._set_operator_in_input, '**(1/2)')

        # Ergebnis der Wissenschaftlichen Funktionstasten.

        self._BTN_PI['command'] = partial(self._set_values_in_input, 'pi')
        self._BTN_SIN['command'] = partial(self._set_values_in_input, 'sin')
        self._BTN_COS['command'] = partial(self._set_values_in_input, 'cos')
        self._BTN_TAN['command'] = partial(self._set_values_in_input, 'tan')
        self._BTN_2PI['command'] = partial(self._set_values_in_input, '2*pi')
        self._BTN_COSH['command'] = partial(self._set_values_in_input, 'cosh')
        self._BTN_TANH['command'] = partial(self._set_values_in_input, 'tanh')
        self._BTN_SINH['command'] = partial(self._set_values_in_input, 'sinh')
        self._BTN_LOG['command'] = partial(self._set_values_in_input, 'log')
        self._BTN_INV['command'] = partial(self._set_values_in_input, '1/')
        self._BTN_MOD['command'] = partial(self._set_values_in_input, '%')
        self._BTN_E['command'] = partial(self._set_values_in_input, 'e')
        self._BTN_LOG2['command'] = partial(self._set_values_in_input, 'log2')
        self._BTN_DEG['command'] = partial(
            self._set_values_in_input, 'degrees')
        self._BTN_ACOSH['command'] = partial(
            self._set_values_in_input, 'acosh')
        self._BTN_ASINH['command'] = partial(
            self._set_values_in_input, 'asinh')
        self._BTN_LOG10['command'] = partial(
            self._set_values_in_input, 'log10')
        self._BTN_LOG1P['command'] = partial(
            self._set_values_in_input, 'log1p')
        self._BTN_EXPM1['command'] = partial(
            self._set_values_in_input, 'expm1')
        self._BTN_LGAMMA['command'] = partial(
            self._set_values_in_input, 'lgamma')
        self._BTN_RAD['command'] = partial(
            self._set_values_in_input, 'radians')
        self._BTN_GAMMA['command'] = partial(
            self._set_values_in_input, 'gamma')
        self._BTN_ERF['command'] = partial(self._set_values_in_input, 'erf')
        self._BTN_ERFC['command'] = partial(self._set_values_in_input, 'erfc')

        # Ereignisse der Funktionstasten des Taschenrechners
        self._BTN_DOT['command'] = partial(self._set_dot_in_input, '.')
        self._BTN_OPEN_PARENT['command'] = self._set_open_parent
        self._BTN_CLOSE_PARENT['command'] = self._set_close_parent
        self._BTN_DEL['command'] = self._del_last_value_in_input
        self._BTN_CLEAR['command'] = self._clear_input
        self._BTN_RESULT['command'] = self._get_data_in_input

    def _set_values_in_input(self, value):
        """Methode, die für die Erfassung des angeklickten und in der Eingabe gesetzten numerischen Wertes verantwortlich ist"""
        if self._entry.get() == 'Error':
            self._entry.delete(0, len(self._entry.get()))

        if self._entry.get() == '0':
            self._entry.delete(0)
            self._entry.insert(0, value)
        elif self._lenght_max(self._entry.get()):
            self._entry.insert(len(self._entry.get()), value)

    def _set_dot_in_input(self, dot):
        """Methode, die für das Setzen des Dezimaltrennzeichens im Wert zuständig ist"""
        if self._entry.get() == 'Error':
            return

        if self._entry.get()[-1] not in '.+-/*' and self._lenght_max(self._entry.get()):
            self._entry.insert(len(self._entry.get()), dot)

    def _set_open_parent(self):
        """Methode zum Setzen der öffnenden Klammern in der Eingabe"""
        if self._entry.get() == 'Error':
            return

        if self._entry.get() == '0':
            self._entry.delete(0)
            self._entry.insert(len(self._entry.get()), '(')
        elif self._entry.get()[-1] in '+-/*' and self._lenght_max(self._entry.get()):
            self._entry.insert(len(self._entry.get()), '(')

    def _set_close_parent(self):
        """Methode zum Setzen der schließenden Klammern in der Eingabe"""
        if self._entry.get() == 'Error':
            return

        if self._entry.get().count('(') <= self._entry.get().count(')'):
            return
        if self._entry.get()[-1] not in '+-/*(' and self._lenght_max(self._entry.get()):
            self._entry.insert(len(self._entry.get()), ')')

    def _clear_input(self):
        """Setzt die Rechnereingabe zurück, löscht sie vollständig und gibt den Wert 0 ein."""
        self._entry.delete(0, len(self._entry.get()))
        self._entry.insert(0, 0)

    def _del_last_value_in_input(self):
        """Löscht die letzte Ziffer in der Eingabe"""
        if self._entry.get() == 'Error':
            return

        if len(self._entry.get()) == 1:
            self._entry.delete(0)
            self._entry.insert(0, 0)
        else:
            self._entry.delete(len(self._entry.get()) - 1)

    def _set_operator_in_input(self, operator):
        """Methode, die für die Erfassung des angeklickten und in der Eingabe gesetzten mathematischen Operators zuständig ist"""
        if self._entry.get() == 'Error':
            return

        if self._entry.get() == '':
            # print('\33[91mUngültige Operation.\33[m'))
            return
        # Vermeiden von aufeinanderfolgenden Wiederholungen von Vorgängen, um Fehler zu vermeiden.
        if self._entry.get()[-1] not in '+-*/' and self._lenght_max(self._entry.get()):
            self._entry.insert(len(self._entry.get()), operator)

    def _get_data_in_input(self):
        """Nimmt die Daten mit allen in der Eingabe enthaltenen Operationen
        um die Berechnung durchzuführen"""
        if self._entry.get() == 'Error':
            return

        result = self.calc.calculation(self._entry.get())
        self._set_result_in_input(result=result)

    def _set_result_in_input(self, result=0):
        """Das Ergebnis der gesamten Operation in der Eingabe mit Pfeilen"""
        if self._entry.get() == 'Error':
            return

        self._entry.delete(0, len(self._entry.get()))
        self._entry.insert(0, result)

    def _lenght_max(self, data_in_input):
        """Überprüfen, ob die Eingabe die maximale Anzahl von Zeichen erreicht hat"""
        if len(str(data_in_input)) >= 15:
            return False
        return True

    def start(self):
        print('\33[92mCalculator Tk Started. . . .\33[m\n')
        self.master.mainloop()

    def _realod_app(self):
        """Startet die Anwendung neu."""
        python = sys.executable  # Ruft den Pfad der ausführbaren Python-Datei ab
        os.execl(python, python, * sys.argv)

    def _exit(self):
        exit()
