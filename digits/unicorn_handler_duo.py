#!/usr/bin/env python3
"""
unicorn hat - show scatter plot of price history
"""
# pylint: disable=C0103,C0301,E0401
from __future__ import print_function
import json
import os
from time import sleep
import unicornhathd
import unicornhat
import smbus
import unicorn_bars_calculate

bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1
unicornhat.set_layout(unicornhat.HAT)
unicornhat.rotation(180)
unicornhat.brightness(1)

unicornhathd.rotation(270)
unicornhathd.brightness(1)

red = [60, 0, 0]
green = [0, 60, 0]
blue = [0, 0, 60]
gray = [45, 45, 45]
blank = [0, 0, 0]

if not os.path.isfile("/home/pi/unicorn.json"):  #instantiate new config file
    unicorn_bars_calculate.ubars_write(8, "unicorn")

if not os.path.isfile("/home/pi/unicornhd.json"):  #instantiate new config file
    unicorn_bars_calculate.ubars_write(16, "unicornhd")

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
    try:  #if has rainbow hat fire 8 bit, otherwise fire 16 bit calculation
        bus.read_byte(112)
        ubars_display()
        print("8-bit unicorn found")        
    except:
        hd_ubars_display()
    file_name = "/home/pi/trigger.foo"
    while True:
        sleep(3)
        if os.path.exists(file_name):
            try:  #if has rainbow hat fire 8 bit, otherwise fire 16 bit calculation
                bus.read_byte(112)
                ubars_display()

            except:
                print("16-found")
                hd_ubars_display()
            os.remove(file_name)
            sleep(3)
