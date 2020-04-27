#!/usr/bin/env python
"""
high level support for doing this and that.
"""
import sys
from time import time, sleep
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

def main():
    """asdasd"""
    #rainbowhat.display.clear()
    sys.stdout.write('total time to change digits:')
    sys.stdout.flush()
    timeing = time()
    vala = int(sys.argv[1])
    valb = int(sys.argv[2])
    counter = 1.0

    if vala > valb:
        stride = -1
    else:
        stride = 1

    for val in range(vala, valb+stride, stride):
        sleep_time = (counter/(abs(vala-valb)+1.0))**1.8*(10.0/(abs(vala-valb)+1.0))
        #print(st)
        sleep(sleep_time)
        if sleep_time > .01:
            rainbowhat.display.print_str(str(val))
            rainbowhat.display.show()

        counter = counter+1.0

    sys.stdout.write(str(time()-timeing))

if __name__ == "__main__":
    main()
