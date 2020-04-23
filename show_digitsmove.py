#!/usr/bin/env python

import sys
from time import time,sleep
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

#rainbowhat.display.clear()

t0 = time()
vala = int(sys.argv[1])
valb = int(sys.argv[2])
x=1.0

if vala > valb:
    stride=-1
else:
    stride=1
#print
for val in range (vala,valb+stride,stride):
    st=(x/(abs(vala-valb)+1))**1.8*(10.0/(abs(vala-valb)+1))
    print(st)
    sleep (st)
    if st > .01:
        rainbowhat.display.print_str(str(val))
        rainbowhat.display.show()

    x=x+1.0

t1 = time()
print 'total time to change digits: %f' %(t1-t0)
