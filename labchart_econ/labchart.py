"""
get trigger pulse timing from a labchart mat file

efish lab
Hokkaido University
Author: Matasaburo Fukutomi
Email: mfukurow@gmail.com
Version: 0.1.0
"""

import tkinter.filedialog
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt


def select_matfile() -> str:
    print("Select a labchart mat file...")
    filepath = tkinter.filedialog.askopenfilename(filetypes=[("mat file", "*.mat")])
    print(f"{filepath} is selected!")
    return filepath
