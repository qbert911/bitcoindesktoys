#!/usr/bin/env python
"""
rainbow hat - touch handler
"""
# pylint: disable=C0116,E1101,W0613
import signal
import os
import rainbowhat
import config_filefunctions
from rainbowhat_ledfunctions import button_light
import unicorn_bars_calculate
rainbowhat.rainbow.set_clear_on_exit(False)
file_name = "/home/pi/trigger.foo"

@rainbowhat.touch.A.press()
def touch_a(channel):
    global flag
    flag = 1
    if config_filefunctions.is_unicornhat_inverted() > -1:
        button_light(1)
        config_filefunctions.zoom_level_up()

@rainbowhat.touch.B.press()
def touch_b(channel):
    global flag
    flag = 1
    if config_filefunctions.is_unicornhat_inverted() > -1:
        button_light(2)
        config_filefunctions.zoom_level_down()

@rainbowhat.touch.C.press()
def touch_c(channel):
    global flag
    flag = 0
    button_light(3)
    config_filefunctions.flip_sound()

@rainbowhat.touch.release()
def release(channel):
    global flag
    button_light(0)
    print (flag)
    if flag and config_filefunctions.is_unicornhat_inverted() > -1:
        if not os.path.exists(file_name):
            unicorn_bars_calculate.ubars_write()
            os.mknod(file_name)

# waits until a signal is received
signal.pause()
