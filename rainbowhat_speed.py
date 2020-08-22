#!/usr/bin/env python
"""rainbowhat - set speed on leds"""
import sys
import smbus
import rainbowhat
from config_filefunctions import is_sound_on
rainbowhat.rainbow.set_clear_on_exit(False)
bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1

def main():
    """asdasd"""
    rainbowhat.rainbow.clear()
    vala = int(sys.argv[1])

    gray = [5, 5, 5]
    yellow = [20, 20, 0]
    red = [20, 0, 0]
    brightness = 0.04

    if is_sound_on():
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
        try:
            bus.read_byte(112)         #check to see if rainbow hat is connected
            rainbowhat.rainbow.show()  #firing this code with unicornhathd connected breaks it
        except:
            1 == 1

if __name__ == "__main__":
    main()
