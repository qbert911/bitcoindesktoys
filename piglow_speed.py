#!/usr/bin/env python
import sys
from piglow import PiGlow

piglow = PiGlow()
vala = min(11, int(sys.argv[1]))
piglow.all(0)
for colour in range(0,6):
    if vala > colour and vala < colour + 7:
        piglow.colour(6-colour, 1)
