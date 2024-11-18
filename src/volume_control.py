# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Control volume of the system using hand gesture
"""

# Project specific imports
from typing import Tuple, List
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL #type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #type: ignore

# Local imports
from . import cv_utils
from .hand_tracker import HandTracker

def get_system_volume_controller():
    """
    Return an instance of the system volume controller
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))
    
VOLUME_CONTROLLER = get_system_volume_controller()
VOLUME_RANGE = VOLUME_CONTROLLER.GetVolumeRange()
# MIN_VOLUME, MAX_VOLUME = VOLUME_RANGE[0], VOLUME_RANGE[1] # in decibels
MIN_VOLUME, MAX_VOLUME = 0, 1

#-----------------------------------------------------------------------------#
#
# Methods to calculate volume
#
#-----------------------------------------------------------------------------#
def calculate_volume(lm1, lm2, lm3) -> float:
    """
    Calculate volume from the given landmarks

    0.17 radians is approximately 10 degrees
    1.22 radians is approximately 70 degrees
    """
    angle = calculate_angle(lm1, lm2, lm3)
    return nominalize_value(angle, (0.17, 1.22), (MIN_VOLUME, MAX_VOLUME))

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
    vector_1 = [lm1.x - lm2.x, lm1.y - lm2.y]
    vector_2 = [lm3.x - lm2.x, lm3.y - lm2.y]
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1) #type: ignore
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2) #type: ignore
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return np.arccos(dot_product)

def nominalize_value(value: float, old_range: Tuple, new_range: Tuple) -> float:
    """
    Nominalize the value between new range

    Args:
        value float: Incoming value
        old_range Tuple: A tuple of old min and old max
        new_range Tuple: New min and max to map to

    rtype:
        float

    Returns:
        Value between new min and max
    """
    return np.interp(value, (old_range), (new_range))

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
    # SetMasterVolumeLevel: if value is in decibels.
    # We use scalar value because, decibels increases the volume
    # lograthimically.
    VOLUME_CONTROLLER.SetMasterVolumeLevelScalar(value, None)

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
                    display_vol = nominalize_value(volume, (MIN_VOLUME, MAX_VOLUME), (0,100))
                    cv_utils.display(img, int(display_vol), (thumb, index))

            quit_video = livefeed.show(img)
            if quit_video:
                break
