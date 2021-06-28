# -*- coding: utf-8 -*-

"""
Gesture Volume Control
Entry point to the module.
"""

# Python built-in imports
import argparse

# Local imports
from . import cv_utils

#-----------------------------------------------------------------------------#
#
# Arguments
#
#-----------------------------------------------------------------------------#
DES = "Gesture Volume Control: Controls system volume using hand gesture."

PARSER = argparse.ArgumentParser(description=DES)

#-----------------------------------------------------------------------------#
#
# Main function: Entry point
#
#-----------------------------------------------------------------------------#
def main() -> None:
    """ Main function. Gets called when the module is called from the cmdline.
    """
    args = PARSER.parse_args()

    with cv_utils.LiveFeed() as livefeed:
        while livefeed.isOpened():
            success, img = livefeed.read()
            if not success:
                break

            quit_video = livefeed.show(img)
            if quit_video:
                break

if __name__ == '__main__':
    main()