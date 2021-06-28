# -*- coding: utf-8 -*-

"""
Gesture Volume Control
Entry point to the module.
"""

# Python built-in imports
import argparse

# Local imports
from .volume_control import volume_control

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
    volume_control()

if __name__ == '__main__':
    main()
