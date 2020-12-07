#!/usr/bin/env python
"""
unicorn hat - show scatter plot of price history
"""
# pylint: disable=C0103,C0301
from __future__ import print_function
import json
import os
from time import sleep
import unicornhat as unicorn
from config_filefunctions import is_unicornhat_inverted
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(abs(is_unicornhat_inverted())*180)   #set to zero for battlestation, 1 for twin display, and -1 for solo
unicorn.brightness(1)

red = [60, 0, 0]
green = [0, 60, 0]
gray = [45, 45, 45]
blank = [0, 0, 0]

def ubars_display():
    """update unicornhat with data from file"""
    displayfile_name = "/home/pi/unicorn.json"
    with open(displayfile_name, 'r') as openfile:
        position = json.load(openfile)

        for y in range(0, 8):
            for x in range(0, 8):
                if position[x][y] == 0:
                    r, g, b = blank
                elif position[x][y] == 1:
                    r, g, b = green
                elif position[x][y] == -1:
                    r, g, b = red
                elif position[x][y] == 8:
                    r, g, b = gray

                unicorn.set_pixel(x, y, r, g, b)
    unicorn.show()
    print(position)

if __name__ == "__main__":
    ubars_display()
    file_name = "/home/pi/trigger.foo"
    while True:
        if os.path.exists(file_name):
            ubars_display()
            os.remove(file_name)
            sleep(1)
