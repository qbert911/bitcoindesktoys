#!/usr/bin/env python
# pylint: disable=C0103,C0326
"""
write to the seven leds on the top of the rainbow HAT
"""
import sys
import rainbowhat

position = [
    [-1,-1,-1,-1,-1,-1,-1],
    [0 ,-1,-1,-1,-1,-1,-1],
    [0 , 0,-1,-1,-1,-1,-1],
    [0 , 0, 0,-1,-1,-1,-1],
    [0 , 0, 0, 0,-1,-1,-1],
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
red = [2, 0, 0]
green = [0, 2, 0]
gray = [1, 1, 1]
blank = [0, 0, 0]
brightness = 1

def rainbow_led_pricechange(vala):
    """asdasd"""
    rainbowhat.rainbow.set_clear_on_exit(False)
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

def rainbow_clear_leds():
    rainbowhat.rainbow.set_clear_on_exit(False)
    rainbowhat.rainbow.clear()
    rainbowhat.rainbow.show()

def rainbow_set_middle_on():
    rainbowhat.rainbow.set_clear_on_exit(False)
    rainbowhat.rainbow.clear()
    rainbowhat.rainbow.set_pixel(3, 5, 5, 5, 0.04)
    rainbowhat.rainbow.show()

def rainbow_show_message(vala):
    rainbowhat.display.clear()

    rainbowhat.display.print_str(vala)
    rainbowhat.display.show()

def button_light(vala):
    if vala == 1:
        rainbowhat.lights.rgb(1, 0, 0)
    elif vala == 2:
        rainbowhat.lights.rgb(0, 1, 0)
    elif vala == 3:
        rainbowhat.lights.rgb(0, 0, 1)
    else:
        rainbowhat.lights.rgb(0, 0, 0)

if __name__ == "__main__":
    rainbow_led_pricechange(sys.argv[1])
    #print ("supposed to be called from another python file, not solo")
