"""
synchronize triggered frame (econ) with triger pulse (labchart)

efish lab
Hokkaido University
Author: Matasaburo Fukutomi
Email: mfukurow@gmail.com
Version: 0.1.0
"""

from scipy.io import savemat, loadmat
import numpy as np
import labchart_econ as le
import os


def sync_labchart_econ(
    videofilepath: str = None,
    matfilepath: str = None,
    intrange: list = None,
    ch: int = 0,
    thr: float = 1,
    save: bool = False,
) -> np.ndarray:
    """
    synchronize triggered frame (econ) with triger pulse (labchart)

    Args:
        videofilepath (str, optional): file path for a video to be analyzed. Defaults to None.
        matfilepath (str, optional): full path to the mat file. Defaults to None.
        intrange (list, optional): [minimum interval, maximum interval]. Defaults to None.
        ch (int, optional): channel number of trigger pulse. Defaults to 0.
        thr (float, optional): threshold to detect pulses. Defaults to 1.
        save (bool, optional): if True, save the output as a mat file. Defaults to False.

    Returns:
        np.ndarray: t_pulse, time information about pulse onset;
                    t_frame, time information about all frames;
                    is_trigframe, bool
    """

    # select a video file (optional)
    if videofilepath is None:
        videofilepath = le.select_videofile()

    # select a labchart mat file (optional)
    if matfilepath is None:
        matfilepath = le.select_matfile()

    # get t_trigframe (time information for triggered frames)
    t_frame = le.read_timestamp(videofilepath)
    t_trigframe, is_trigframe = le.get_t_trig_frame(t_frame, intrange)

    # get t_pulse (time information for trigger pulses)
    chtrig, ts = le.read_chtrig(matfilepath, ch)
    t_pulse, _ = le.get_t_trig_pulse(chtrig, ts, thr)

    # compare numbers between t_trigframe and t_pulse
    n_trigframe = t_trigframe.shape[0]
    n_pulse = t_pulse.shape[0]
    print(f"number of triggered frame: {n_trigframe}")
    print(f"number of trigger pulse: {n_pulse}")
    if n_trigframe == n_pulse:
        print("Congraturations!")
    else:
        print("Numbers are different. Something was wrong...")

    # save (optional)
    if save:
        data = {
            "t_pulse": t_pulse,
            "t_frame": t_frame,
            "is_trigframe": is_trigframe,
            "videofilepath": videofilepath,
            "matfilepath": matfilepath,
        }
        outfilename = os.path.splitext(matfilepath)[0] + "_trig.mat"
        savemat(outfilename, data)

    return t_pulse, t_frame, is_trigframe
