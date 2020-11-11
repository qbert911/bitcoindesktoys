#!/usr/bin/env python
"""
unicorn hat - show scatter plot of price history
"""
# pylint: disable=C0103,C0301
from __future__ import print_function
import csv
import os
import math
import json
from time import sleep
import unicornhathd

unicornhathd.rotation(270)
unicornhathd.brightness(1)

red = [60, 0, 0]
green = [0, 60, 0]
blue = [0, 0, 60]
gray = [45, 45, 45]
blank = [0, 0, 0]

def hd_ubars_display_old():
    """update unicornhat with data from file"""
    unicornhathd.clear()
    displayfile_name = "/home/pi/hdbars.csv"
    with open(displayfile_name, 'r') as openfile:
        position = next(csv.reader(openfile))
        endzeros = 0
        for x in range(1, 15):
            if int(position[16-x]) != 0:
                break
            endzeros += 1
        amount = int(position[16-x])
        for x in range(1, endzeros+2):
            position[16-x] = math.floor(amount/(endzeros+1))
        position[16-x] = amount-(endzeros*math.floor(amount/(endzeros+1)))
        for x in range(0, 16):
            for y in range(0, min(int(position[x]), 16)):
                r, g, b = gray
                unicornhathd.set_pixel(x, y, r, g, b)
            for y in range(0, max(min(int(position[x])-16, 16), 0)):
                r, g, b = green
                unicornhathd.set_pixel(x, y, r, g, b)
            for y in range(0, max(min(int(position[x])-32, 16), 0)):
                r, g, b = blue
                unicornhathd.set_pixel(x, y, r, g, b)
            for y in range(0, max(min(int(position[x])-48, 16), 0)):
                r, g, b = red
                unicornhathd.set_pixel(x, y, r, g, b)

    if round(float(position[16])) <= 7 or int(position[0]) > 20:
        r, g, b = red
    else:
        r, g, b = green
    unicornhathd.set_pixel(0, min(round(float(position[16])-1), 15), r, g, b)
    unicornhathd.show()
    print(position, round(float(position[16])-1), endzeros)


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

                unicornhathd.set_pixel(x, y, r, g, b)
    unicornhathd.show()
    print(position)

if __name__ == "__main__":
    hd_ubars_display()
    file_name = "/home/pi/triggerhd.foo"
    while True:
        if os.path.exists(file_name):
            hd_ubars_display()
            os.remove(file_name)
            sleep(3)
