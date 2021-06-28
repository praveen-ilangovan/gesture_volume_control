# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Uses mediapipe module to track hands
"""

# Project specific imports
import mediapipe as mp #type: ignore
from typing import List

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
    def get_finger_tips(self, landmarks) -> List:
        """
        Get the landmarks: Thumb Tip, Thumb base and Index Tip

        rtype:
            List
        
        Return:
            A list of landmarks
        """
        if len(landmarks.landmark) < HandTracker.INDEX_FINGER_TIP:
            return []

        return [landmarks.landmark[HandTracker.THUMB_TIP],
                landmarks.landmark[HandTracker.THUMB_CMC],
                landmarks.landmark[HandTracker.INDEX_FINGER_TIP]]
