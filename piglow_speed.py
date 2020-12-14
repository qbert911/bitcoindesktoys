#!/usr/bin/env python3
"""
test
"""
import sys
import piglow

piglow.clear_on_exit = False

vala = min(11, int(sys.argv[1]))

try:
    piglow.all(0)
    for colour in range(0, 6):
        if colour + 7 > vala > colour:
            piglow.colour(6-colour, 1)
    piglow.show()
except:
    pass
    #print("exception")
