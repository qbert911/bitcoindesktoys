#!/usr/bin/env python
"""
high level support for doing this and that.
"""
import os, sys
with open(os.devnull, 'w') as f:   #to prevent pygame loading message
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f

    from pygame import mixer

    # enable stdout
    sys.stdout = oldstdout

from time import time, sleep
from rainbowhat_ledfunctions import rainbow_led_pricechange

import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

mixer.pre_init(buffer=1024)
mixer.init()
soundup = mixer.Sound('/home/pi/bitcoindesktoys/tickup.wav')
sounddown = mixer.Sound('/home/pi/bitcoindesktoys/tickdown.wav')

def main():
    """asdasd"""
    #rainbowhat.display.clear()
    sys.stdout.write('total time to change digits:')
    sys.stdout.flush()
    timeing = time()
    vala = int(sys.argv[1])
    valb = int(sys.argv[2])
    valc = int(sys.argv[3])
    counter = 1.0

    if vala > valb:
        stride = -1
    else:
        stride = 1

    for val in range(vala, valb+stride, stride):
        sleep_time = (counter/(abs(vala-valb)+1.0))**1.8*(10.0/(abs(vala-valb)+1.0))
        #print(sleep_time,val)
        sleep(sleep_time)
        if sleep_time > .01:
            rainbowhat.display.print_str(str(val))
            rainbowhat.display.show()

        if val > vala:
            soundup.play()
        elif val < vala:
            sounddown.play()

        counter = counter+1.0
    rainbow_led_pricechange(valc)
    sys.stdout.write(str(time()-timeing))

if __name__ == "__main__":
    main()
    sleep(1)   #needed so we can hear the last sound effect
