#!/usr/bin/env python
"""
write to the seven leds on the top of the rainbow HAT
"""
from os import system
from time import sleep
from picamera import PiCamera
camera = PiCamera()
#camera.resolution = (480, 720)


totalpics = 180
delay = 4

print "taking", totalpics, "pictures total    every", delay, "seconds     for a total of", totalpics*delay/60/60.00, "hours"

for i in range(totalpics):
    camera.capture('pics/image{0:04d}.jpg'.format(i))
    print 'pics/image{0:04d}.jpg'.format(i)," / ",totalpics
    sleep(delay)

 #.\ffmpeg -framerate 6 -i 'D:\share\bitcoindesktoys\pics-1\image%04d.jpg' -c:v libx264 d:\share\out.mp4
