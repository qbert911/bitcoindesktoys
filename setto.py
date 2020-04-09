#!/usr/bin/env python

import sys
import time
import rainbowhat

rainbowhat.rainbow.set_clear_on_exit(False)
rainbowhat.rainbow.clear()
vala = int(sys.argv[1])

red=[255, 0, 0]
green=[0, 255, 0]
gray=[25, 25, 30]
brightness=0.04

for x in range(0,7):
    if vala > x:
        r,g,b=gray
        rainbowhat.rainbow.set_pixel( (6-x), r,g,b,brightness)

for x in range(8,15):
    if vala >= x:
        r,g,b=green
        rainbowhat.rainbow.set_pixel( (14-x), r,g,b,brightness)

for x in range(16,23):
    if vala >= x:
        r,g,b=red
        rainbowhat.rainbow.set_pixel( (22-x), r,g,b,brightness)

rainbowhat.rainbow.show()
