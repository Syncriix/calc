# -*- coding: utf-8 -*-

# @autor: Sebastian Rohner
# @github: github.com/Syncriix

# Builtin
import tkinter as tk

# Local
from app.Calculator import Calculator

if __name__ == '__main__':
    master = tk.Tk()
    main = Calculator(master)
    main.start()
