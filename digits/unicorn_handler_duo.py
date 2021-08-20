#!/usr/bin/env python3
"""
unicorn hat - show scatter plot of price history
"""
# pylint: disable=C0103,C0301
from __future__ import print_function
import json
import os
from time import sleep
import unicornhathd
import unicornhat
from config_filefunctions import is_unicornhat_inverted
unicornhat.set_layout(unicornhat.HAT)
unicornhat.rotation(abs(is_unicornhat_inverted())*180)   #set to zero for battlestation, 1 for twin display, and -1 for solo
unicornhat.brightness(1)

unicornhathd.rotation(270)
unicornhathd.brightness(1)

red = [60, 0, 0]
green = [0, 60, 0]
blue = [0, 0, 60]
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

                unicornhat.set_pixel(x, y, r, g, b)
    unicornhat.show()
    print(position)

def hd_ubars_display():
    """update unicornhat with data from file"""
    displayfile_name = "/home/pi/unicornhd.json"
    unicornhathd.clear()
    with open(displayfile_name, 'r') as openfile:
        position = json.load(openfile)

        for y in range(0, 16):
            for x in range(0, 16):
                if position[x][y] == 0:
                    r, g, b = blank
                elif position[x][y] == 1:
                    r, g, b = green
                elif position[x][y] == -1:
                    r, g, b = red
                elif position[x][y] == 8:
                    r, g, b = gray

                unicornhathd.set_pixel(x, 15-y, r, g, b)
    unicornhathd.show()
    print(position)

if __name__ == "__main__":
    ubars_display()
    hd_ubars_display()
    file_name2 = "/home/pi/triggerhd.foo"
    file_name = "/home/pi/trigger.foo"
    while True:
        sleep(3)
        if os.path.exists(file_name):
            ubars_display()
            os.remove(file_name)
            sleep(3)
        if os.path.exists(file_name2):
            hd_ubars_display()
            os.remove(file_name2)
            sleep(3)
