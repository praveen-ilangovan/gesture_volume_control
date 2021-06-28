# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Control volume of the system using hand gesture
"""

# Python built-ins
import math

# Project specific imports
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume #type: ignore

# Local imports
from . import cv_utils
from .hand_tracker import HandTracker

#-----------------------------------------------------------------------------#
#
# Methods to calculate volume
#
#-----------------------------------------------------------------------------#
def calculate_volume(lm1, lm2, lm3) -> float:
    """
    Calculate volume from the given landmarks
    """
    angle = calculate_angle(lm1, lm2, lm3)
    return nominalize_value(angle)

def calculate_angle(lm1, lm2, lm3) -> float:
    """
    Given three points, calculate the angle.
    lm1 -> Thumb Tip
    lm2 -> Thumb Base
    lm3 -> Index Tip

    rtype:
        float

    Return:
        Angle between three points in radians
    """
    p1 = (lm1.x - lm2.x, lm1.y - lm2.y)
    p2 = (lm3.x - lm2.x, lm3.y - lm2.y)

    dot = (p1[0]*p2[0]) + (p1[1]*p2[1])
    mag_p1 = math.sqrt(p1[0]**2 + p1[1]**2)
    mag_p2 = math.sqrt(p2[0]**2 + p2[1]**2)

    return math.acos(dot/(mag_p1*mag_p2))

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
    value = min(max_value, max(min_value, value)) 
    return (value - min_value) / (max_value - min_value)

#-----------------------------------------------------------------------------#
#
# Methods to control the volume
#
#-----------------------------------------------------------------------------#
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

    Press 'q' to quit the live feed
    """
    hand_tracker = HandTracker()

    with cv_utils.LiveFeed() as livefeed:
        while livefeed.isOpened():
            success, img = livefeed.read()
            if not success:
                break

            img_rgb = cv_utils.convert_to_rgb(img)
            results = hand_tracker.hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    finger_tips = hand_tracker.get_finger_tips(landmarks)
                    if not finger_tips:
                        continue

                    thumb, base, index = finger_tips

                    # Set the volume
                    volume = calculate_volume(thumb, base, index)
                    set_volume(volume)

                    # Display the information
                    cv_utils.display(img, volume, (thumb, index))

            quit_video = livefeed.show(img)
            if quit_video:
                break
