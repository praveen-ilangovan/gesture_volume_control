# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Control volume of the system using hand gesture
"""

# Project specific imports
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume #type: ignore

# Local imports
from . import cv_utils
from .hand_tracker import HandTracker

#-----------------------------------------------------------------------------#
#
# Methods to control the volume
#
#-----------------------------------------------------------------------------#
def nominalize_value(value: float, min_value: float=0.17, max_value: float=1.22) -> float:
    """
    Nominalize the value between 0 and 1
    0.17 radians is approximately 10 degrees
    1.22 radians is approximately 70 degrees

    Args:
        value float: Incoming value
        min_value float: Minimum value.. will be nominalized to 0
        max_value float: Maxmimum value.. will be nominalized to 1

    rtype:
        float

    Returns:
        Nominalized value betwen 0 and 1
    """
    if value < min_value:
        return 0
    elif value > max_value:
        return 1
    
    return (value - min_value) / (max_value - min_value)

def set_volume(value: float) -> None:
    """
    Set the volume of the system.

    Args:
        value float: volume
    """
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process:
            volume.SetMasterVolume(value, None)

def volume_control():
    """
    Track the hand gesture and control the volume of the system.
    When the angle between thumb tip and index finger tip is 10 degrees
    or less, the volume will be set to 0 and if it is greater than
    70 degrees, the volume will be set to 1.
    """
    hand_tracker = HandTracker()

    with cv_utils.LiveFeed() as livefeed:
        while livefeed.isOpened():
            success, img = livefeed.read()
            if not success:
                break

            results = hand_tracker.process(img)
            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:

                    value = hand_tracker.calculate_angle(landmarks)
                    volume = nominalize_value(value)
                    set_volume(volume)

                    hand_tracker.draw_landmarks(img, landmarks)

            quit_video = livefeed.show(img)
            if quit_video:
                break