#!/usr/bin/env python

import sys
from time import time,sleep
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

#rainbowhat.display.clear()
sys.stdout.write('total time to change digits:')
sys.stdout.flush()
t0 = time()
vala = int(sys.argv[1])
valb = int(sys.argv[2])
x=1.0

if vala > valb:
    stride=-1
else:
    stride=1

for val in range (vala,valb+stride,stride):
    st=(x/(abs(vala-valb)+1.0))**1.8*(10.0/(abs(vala-valb)+1.0))
    #print(st)
    sleep (st)
    if st > .01:
        rainbowhat.display.print_str(str(val))
        rainbowhat.display.show()

    x=x+1.0

sys.stdout.write(str(time()-t0))
