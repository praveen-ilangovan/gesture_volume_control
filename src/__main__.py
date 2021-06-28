# -*- coding: utf-8 -*-

"""
Gesture Volume Control
Entry point to the module.
"""

# Python built-in imports
import argparse

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
    print("Controls the system volume with hand gesture")

if __name__ == '__main__':
    main()