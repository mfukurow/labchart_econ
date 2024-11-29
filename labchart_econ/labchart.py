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


def select_matfile() -> str:
    """
    show a diagram to select a labchart mat file

    Returns:
        str: full path to the mat file
    """
    print("Select a labchart mat file...")
    filepath = tkinter.filedialog.askopenfilename(filetypes=[("mat file", "*.mat")])
    print(f"{filepath} is selected!")
    return filepath


def read_chtrig(matfilepath: str, ch: int = 0) -> np.ndarray:
    """
    read a labchart mat file and extract trigger channel and time information

    Args:
        matfilepath (str): full path to the mat file
        ch (int, optional): channel number of trigger pulse. Defaults to 0.

    Returns:
        np.ndarray: trigger channel (1st item) and time (2nd item)
    """
    matdata = loadmat(matfilepath)
    chtrig = np.array(matdata["data_block1"][ch,])
    ts = np.array(matdata["ticktimes_block1"][0,])
    return chtrig, ts


def get_t_pulse(chtrig: np.ndarray, ts: np.ndarray, thr: float = 1) -> np.ndarray:
    """
    get time information about trigger pulse

    Args:
        chtrig (np.ndarray): trigger channel
        ts (np.ndarray): time information corresponding to the trigger channel
        thr (float, optional): threshold to detect pulses. Defaults to 1.

    Returns:
        np.ndarray: trigger pulse time (1st item) and bool indicating trigger
                    (2nd item; True, trigger; False, not trigger)
    """
    idx_high = np.where(chtrig > thr)[0]
    idx_pulse = np.concatenate(
        [np.array([idx_high[0]]), idx_high[np.where(np.diff(idx_high) > 1)[0] + 1]]
    )
    t_pulse = ts[idx_pulse]
    return t_pulse, idx_pulse
