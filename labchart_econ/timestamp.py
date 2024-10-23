"""
git timestamp data from a video

efish lab
Hokkaido University
Author: Matasaburo Fukutomi
Email: mfukurow@gmail.com
Version: 0.1.1
"""

import cv2
import numpy as np
import tkinter.filedialog
import matplotlib.pyplot as plt


def select_videofile() -> str:
    """
    show a diagram to select a video file

    Returns:
        str: full path to the video file
    """
    print("Select a video file...")
    filepath = tkinter.filedialog.askopenfilename()
    print(f"{filepath} is selected!")
    return filepath


def get_timestamp(videofilepath: str = None) -> np.ndarray:
    """
    extract timestamp information from a video

    Args:
        videofilepath (str): file path for a video to be analyzed

    Returns:
        np.ndarray: a vector of timestamps
    """
    if videofilepath is None:
        videofilepath = select_videofile()

    cap = cv2.VideoCapture(videofilepath)
    timestamp = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    while cap.isOpened():
        frame_exist, curr_frame = cap.read()
        if not frame_exist:
            break
        timestamp_current = cap.get(cv2.CAP_PROP_POS_MSEC)
        timestamp.append(timestamp_current)
    cap.release()
    timestamp = np.array(timestamp[1 : len(timestamp)]) / 1000  # msec -> sec
    return timestamp


def plt_ifi(timestamp: np.ndarray, is_trig: np.ndarray = None) -> None:
    """
    plot inter-frame interval

    Args:
        timestamp (np.ndarray): timestamp acquired by get_timestamp
        is_trig (np.ndarray, optional): True, trigger; False, not trigger
    """
    interval = np.diff(timestamp)
    time = timestamp[1 : len(timestamp)]
    _, ax = plt.subplots()
    ax.scatter(time, interval)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Inter-frame interval (s)")
    # highlight the triggered frames (optional)
    if is_trig is not None:
        ax.scatter(time[is_trig[1 : len(is_trig)]], interval[is_trig[1 : len(is_trig)]])
    plt.show()


def is_triggerframe(timestamp: np.ndarray, intrange: list = None) -> np.ndarray:
    """
    make a list of triggered frame (True) and untriggered frame (False)

    Args:
        timestamp (np.ndarray): timestamp acquired by get_timestamp
        intrange (list, optional): [minimum interval, maximum interval]

    Returns:
        np.ndarray: True, trigger; False, not trigger
    """
    if intrange is None:
        print(
            """
Look at the plot and determine the interval range
              """
        )
        plt_ifi(timestamp)
        intrange0 = input(
            """
Enter the interval range
e.g.) 0.005, 0.006

interval range = """
        )
        intrange = [float(num) for num in intrange0.split(",")]

    interval = np.diff(timestamp)
    is_trig0 = np.array([intrange[0] < x < intrange[1] for x in interval])
    idx_firsttrig = np.argmax(is_trig0)
    is_trig0[idx_firsttrig - 1] = True
    is_trig = np.concatenate([np.array([False]), is_trig0])
    return is_trig
