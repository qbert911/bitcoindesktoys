#!/usr/bin/env python
"""jjjjj"""
import sys
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)
# pylint: disable=C0103,C0326

rainbowhat.rainbow.clear()
vala = int(sys.argv[1])+10
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
red = [55, 0, 0]
green = [0, 55, 0]
gray = [25, 25, 30]
blank = [0,0,0]
brightness = 0.04

def main():
    """asdasd"""
    #print position[vala]
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
    main()
