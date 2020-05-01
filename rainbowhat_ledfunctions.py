#!/usr/bin/env python
# pylint: disable=C0103,C0326
"""
write to the seven leds on the top of the rainbow HAT
"""
import rainbowhat

position = [
    [-1,-1,-1,-1,-1,-1,-1],
    [0,-1,-1,-1,-1,-1,-1],
    [0,0,-1,-1,-1,-1,-1],
    [0,0,0,-1,-1,-1,-1],
    [0,0,0,0,-1,-1,-1],
    [0,0,0,0,0,-1,-1],
    [0,0,0,0,0,0,-1],
    [-1,-1,-1,2,0,0,0],
    [0,-1,-1,2,0,0,0],
    [0,0,-1,2,0,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,2,+1,0,0],
    [0,0,0,2,+1,+1,0],
    [0,0,0,2,+1,+1,+1],
    [+1,0,0,0,0,0,0],
    [+1,+1,0,0,0,0,0],
    [+1,+1,+1,0,0,0,0],
    [+1,+1,+1,+1,0,0,0],
    [+1,+1,+1,+1,+1,0,0],
    [+1,+1,+1,+1,+1,+1,0],
    [+1,+1,+1,+1,+1,+1,+1]
]
red = [20, 0, 0]
green = [0, 20, 0]
gray = [10, 10, 20]
blank = [0,0,0]
brightness = 0.04

def rainbow_led_pricechange(vala):
    """asdasd"""
    rainbowhat.rainbow.clear()
    #print position[vala]
    vala=int(vala)+10
    for x in range(0,7):
        if position[vala][x] == 2:
            r,g,b = gray
        elif position[vala][x] == -1:
            r,g,b = red
        elif position[vala][x] == +1:
            r,g,b = green
        else:
            r,g,b = blank
        rainbowhat.rainbow.set_pixel(6-x, r,g,b,brightness)

    rainbowhat.rainbow.show()

if __name__ == "__main__":
    print ("supposed to be called from another python file, not solo")
