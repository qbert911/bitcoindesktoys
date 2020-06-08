#!/usr/bin/env python
"""
rainbow HAT - alter digits and call led function
"""
import os
import sys

with open(os.devnull, 'w') as f:   #to prevent pygame loading message
    oldstdout = sys.stdout
    sys.stdout = f
    from pygame import mixer
    sys.stdout = oldstdout
#------------end pygame non display message hack------------------------------
mixer.pre_init(buffer=8192)
mixer.init()
soundup = mixer.Sound('/home/pi/bitcoindesktoys/tickup.wav')
soundup.play()
