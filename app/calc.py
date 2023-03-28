# -*- coding: utf-8 -*-

# @autor: Sebastian Rohner
# @github: github.com/Syncriix

from math import pi, cos, sin, tan, acos, asin, atan, sqrt, log, log10, exp, factorial, pow, e, tau, inf, nan


class Calc:
    """Klasse, die für die Durchführung aller Berechnungen im Taschenrechner verantwortlich ist"""

    def calculation(self, calc):
        """Verantwortlich für die Entgegennahme der auszuführenden Berechnung, Rückgabe
        des Ergebnisses oder einer Fehlermeldung im Falle eines Fehlers.
        """
        return self.__calculation_validation(calc=calc)

    def __calculation_validation(self, calc):
        """Verantwortlich für die Überprüfung, ob die angegebene Berechnung durchgeführt werden kann"""
        result = eval(calc)
        try:
            print(eval(calc))

            return self.__format_result(result=result)
        except (NameError, ZeroDivisionError, SyntaxError, ValueError):
            return 'Error'

    def __format_result(self, result):
        """Formatiert das Ergebnis in wissenschaftlicher Notation, wenn es zu groß ist
        und gibt den formatierten Wert im String-Typ zurück"""

        result = str(result)
        if len(result) > 15:
            result = '{:5.5E}'.format(float(result))

        return result
