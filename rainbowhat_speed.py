#!/usr/bin/env python
"""asdasd"""
import sys
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

# pylint: disable=C
def main():
    """asdasd"""
    rainbowhat.rainbow.clear()
    vala = int(sys.argv[1])

    red = [20, 0, 0]
    yellow = [20, 20, 0]
    gray = [5, 5, 5]
    #blank = [0,0,0]
    brightness = 0.04

    for valuetocheck in range(0, 7):
        if vala > valuetocheck:
            r, g, b = gray
            rainbowhat.rainbow.set_pixel((6-valuetocheck), r, g, b, brightness)

    for valuetocheck in range(8, 15):
        if vala >= valuetocheck:
            r, g, b = yellow
            rainbowhat.rainbow.set_pixel((14-valuetocheck), r, g, b, brightness)

    for valuetocheck in range(16, 23):
        if vala >= valuetocheck:
            r, g, b = red
            rainbowhat.rainbow.set_pixel((22-valuetocheck), r, g, b, brightness)

    rainbowhat.rainbow.show()

if __name__ == "__main__":
    main()
