# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Uses mediapipe module to track hands
"""

# Builtins
from __future__ import annotations
import math

# Project specific imports
import mediapipe as mp #type: ignore
import numpy as np

# Local imports
from . import cv_utils

#-----------------------------------------------------------------------------#
#
# MediaPipe HandTracker
#
#-----------------------------------------------------------------------------#
class HandTracker():

    THUMB_CMC = 1
    THUMB_TIP = 4
    INDEX_FINGER_TIP = 8

    def __init__(self, max_hands: int=1):
        super().__init__()
        self.__mp_hands = mp.solutions.hands
        self.__mp_draw = mp.solutions.drawing_utils

        self.__hands = self.__mp_hands.Hands(max_num_hands=max_hands)

    #--------------------------------------------------------------------------#
    # Properties
    #--------------------------------------------------------------------------#
    @property
    def hands(self):
        return self.__hands

    #--------------------------------------------------------------------------#
    # Methods
    #--------------------------------------------------------------------------#
    def process(self, img: np.ndarray):
        """
        Convert the img from BGR to RGB and color space and pass it
        over to the mediapipe to process it.

        Args:
            img np.ndarray: Image in numpy array format

        rtype:
            mediapipe landmarks

        Return:
            A list of 21 landmarks in the hand
        """
        img_rgb = cv_utils.convert_to_rgb(img)
        return self.__hands.process(img_rgb)

    def calculate_angle(self, landmarks) -> float:
        """
        Calculate the angle between THUMB_TIP and INDEX_TIP

        rtype:
            float

        Return:
            Angle between these points in radians
        """
        if len(landmarks.landmark) > HandTracker.INDEX_FINGER_TIP:
            lm1 = landmarks.landmark[HandTracker.THUMB_TIP]
            lm2 = landmarks.landmark[HandTracker.THUMB_CMC]
            lm3 = landmarks.landmark[HandTracker.INDEX_FINGER_TIP]

        p1 = (lm1.x - lm2.x, lm1.y - lm2.y)
        p2 = (lm3.x - lm2.x, lm3.y - lm2.y)

        dot = (p1[0]*p2[0]) + (p1[1]*p2[1])
        mag_p1 = math.sqrt(p1[0]**2 + p1[1]**2)
        mag_p2 = math.sqrt(p2[0]**2 + p2[1]**2)

        return math.acos(dot/(mag_p1*mag_p2))

    def draw_landmarks(self, img: np.ndarray, landmarks) -> None:
        """
        Draw the landmarks in the image

        Args:
            img np.ndarray: Image in numpy array format
        """
        self.__mp_draw.draw_landmarks(img, landmarks,
            self.__mp_hands.HAND_CONNECTIONS)
