"""
get t_frame data from a video

efish lab
Hokkaido University
Author: Matasaburo Fukutomi
Email: mfukurow@gmail.com
Version: 0.1.0
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
    filepath = tkinter.filedialog.askopenfilename(
        filetypes=[("mp4 file", "*.mp4"), ("avi file", "*.avi")]
    )
    print(f"{filepath} is selected!")
    return filepath


def read_timestamp(videofilepath: str) -> np.ndarray:
    """
    extract timestamp (t_frame) information from a video

    Args:
        videofilepath (str): file path for a video to be analyzed

    Returns:
        np.ndarray: a vector of timestamps
    """
    cap = cv2.VideoCapture(videofilepath)
    t_frame = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    while cap.isOpened():
        frame_exist, curr_frame = cap.read()
        if not frame_exist:
            break
        timestamp_current = cap.get(cv2.CAP_PROP_POS_MSEC)
        t_frame.append(timestamp_current)
    cap.release()
    t_frame = np.array(t_frame[1 : len(t_frame)]) / 1000  # msec -> sec
    return t_frame


def plt_ifi(t_frame: np.ndarray, is_trigframe: np.ndarray = None) -> None:
    """
    plot inter-frame interval

    Args:
        t_frame (np.ndarray): t_frame acquired by read_timestamp
        is_trigframe (np.ndarray, optional): True, trigger; False, not trigger
    """
    interval = np.diff(t_frame)
    time = t_frame[1 : len(t_frame)]
    _, ax = plt.subplots()
    ax.scatter(time, interval)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Inter-frame interval (s)")
    # highlight the triggered frames (optional)
    if is_trigframe is not None:
        ax.scatter(
            time[is_trigframe[1 : len(is_trigframe)]],
            interval[is_trigframe[1 : len(is_trigframe)]],
        )
    plt.show()


def get_t_trigframe(t_frame: np.ndarray, intrange: list = None) -> np.ndarray:
    """
    make a list of triggered frame (True) and untriggered frame (False)

    Args:
        t_frame (np.ndarray): t_frame acquired by read_timestamp
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
        plt_ifi(t_frame)
        intrange0 = input(
            """
Enter the interval range
e.g.) 0.005, 0.006

interval range = """
        )
        intrange = [float(num) for num in intrange0.split(",")]

    interval = np.diff(t_frame)
    is_trig0 = np.array([intrange[0] < x < intrange[1] for x in interval])
    idx_firsttrig = np.argmax(is_trig0)
    is_trig0[idx_firsttrig - 1] = True
    is_trigframe = np.concatenate([np.array([False]), is_trig0])
    t_trigframe = t_frame[is_trigframe]
    return t_trigframe, is_trigframe
