#!/usr/bin/env python

import sys
import time
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

#rainbowhat.display.clear()

vala = int(sys.argv[1])
valb = int(sys.argv[2])
x=1.0

if vala > valb:
    stride=-1
else:
    stride=1
#print
for val in range (vala,valb+stride,stride):
    st=(x/(abs(vala-valb+stride)))**1.8*(10.0/(abs(vala-valb+stride)))
    print(st)
    time.sleep (st)
    if st > .01:
        rainbowhat.display.print_str(str(val))
        rainbowhat.display.show()

    x=x+1.0
