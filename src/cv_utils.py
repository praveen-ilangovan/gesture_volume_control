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
from typing import Union, Optional, Tuple

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

#-----------------------------------------------------------------------------#
#
# Image processing
#
#-----------------------------------------------------------------------------#
def convert_to_rgb(img: np.ndarray) -> np.ndarray:
    """ Convert the image's colour space to rgb

    Args:
        img numpy.ndarray: Image in an numpy array format

    rtype:
        numpy.ndarray

    Returns:
        A numpy array
    """
    return cv.cvtColor(img, cv.COLOR_BGR2RGB)

def display(img: np.ndarray, volume: float, landmarks: Tuple):
    """
    Display the landmarks and volume information in the image
    """
    height, width, channel = img.shape
    color = (128,0,128)

    # Display the volume
    volume = int(volume*100)
    cv.putText(img, "Volume: {0}".format(volume), (10, height-20),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)

    # Draw the finger tips
    tips = []
    for lm in landmarks:
        cx, cy = (int(lm.x*width), int(lm.y*height))
        tips.append((cx,cy))
        # Draw a circle around the tip
        cv.circle(img, (cx,cy), 10, color, cv.FILLED)

    # Draw the connection line
    cv.line(img, tips[0], tips[1], color, 2)
