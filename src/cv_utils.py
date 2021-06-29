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

def display(img: np.ndarray, volume: int, landmarks: Tuple):
    """
    Display the landmarks and volume information in the image
    """
    height, width, channel = img.shape
    color = (128,0,128)

    # Volume color
    vol_color = (0,255,0)
    if volume < 10:
        vol_color = (0,128,0)
    elif volume > 90:
        vol_color = (0,0,255)

    # Display the volume
    cv.putText(img, "Volume: {0}".format(volume), (10, height-20),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, vol_color, 2)

    # Volume Bar
    volume_bar_width = 200
    volume_bar_height = 20
    volume_bar_origin = (10, height-50)
    volume_bar_dest = (volume_bar_origin[0] + volume_bar_width,
                       volume_bar_origin[1] - volume_bar_height)
    cv.rectangle(img, volume_bar_origin, volume_bar_dest, vol_color, 1)
    cv.rectangle(img, volume_bar_origin, ((volume*2)+volume_bar_origin[0], volume_bar_dest[1]), vol_color, cv.FILLED)

    # Draw the finger tips
    tips = []
    for lm in landmarks:
        cx, cy = (int(lm.x*width), int(lm.y*height))
        cv.circle(img, (cx,cy), 15, color, cv.FILLED)
        tips.append((cx,cy))

    # Draw the connection line
    cv.line(img, tips[0], tips[1], color, 2)

    # Draw the center circle
    cx = tips[0][0] + ((tips[-1][0]-tips[0][0])//2)
    cy = tips[0][1] + ((tips[-1][1]-tips[0][1])//2)
    cv.circle(img, (cx,cy), 15, vol_color, cv.FILLED)
