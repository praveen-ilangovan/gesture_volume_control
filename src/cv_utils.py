# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Module that has all the opencv functionalities used in this
project.
"""

# Builtins
from __future__ import annotations

# Project specific imports
import cv2 as cv #type: ignore
import numpy as np
from typing import Union, Optional

#-----------------------------------------------------------------------------#
#
# Cv VideoCapture as Context Manager
#
#-----------------------------------------------------------------------------#
class VideoCapture(cv.VideoCapture):
    def __init__(self, filepath_or_index: Union[str,int],
                       apipref: Optional[int]=None,
                       waittime: int=1,
                       quitkey: str="q"):
        """ Extends cv.VideoCapture to be used as context manager.

        Args:
            filepath_or_index str|int: Filepath/Index
            apipref int|None: Prefered Capture API backends
            waittime int: Wait time to show the image
            quitkey str: Keyboard character to press to quit capturing

        rtype:
            VideoCapture

        Returns:
            An instance of VideoCapture
        """
        super().__init__(filepath_or_index, apipref)
        self.__waittime = waittime
        self.__quitkey = ord(quitkey)

    #-------------------------------------------------------------------------#
    # Context managers
    #-------------------------------------------------------------------------#
    def __enter__(self) -> VideoCapture:
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.release()
        cv.destroyAllWindows()

    #-------------------------------------------------------------------------#
    # Extended methods
    #-------------------------------------------------------------------------#
    def show(self, img: np.ndarray, winname: str="Video") -> bool:
        """
        Show the image in a window and listen to the keyboard events to stop
        showing.

        Args:
            img np.ndarray: Image in numpy array format
            winname str: Optionally name the window

        rtype:
            bool

        Returns:
            Returns True if quit key is pressed
        """
        # Display the video
        cv.imshow(winname, img)

        # Keep track of the keyboard events. Listen for q key press
        key = cv.waitKey(self.__waittime) & 0xFF
        return key == self.__quitkey
    
#-----------------------------------------------------------------------------#
# LiveFeed from webcam
#-----------------------------------------------------------------------------#
class LiveFeed(VideoCapture):
    def __init__(self, webcam: int=0):
        super().__init__(webcam, cv.CAP_DSHOW)