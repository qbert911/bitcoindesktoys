#!/usr/bin/env python
"""
rainbow hat - touch handler
"""
# pylint: disable=C0116,E1101,W0613
import signal
import os
from rainbowhat import lights, touch
import config_filefunctions
import unicorn_bars_calculate
#rainbowhat.rainbow.set_clear_on_exit(False)
file_name = "/home/pi/trigger.foo"

@touch.A.press()
def touch_a(channel):
    global flag
    flag = 1
    if config_filefunctions.is_unicornhat_inverted() > -1:
        config_filefunctions.zoom_level_up()

@touch.B.press()
def touch_b(channel):
    global flag
    flag = 1
    if config_filefunctions.is_unicornhat_inverted() > -1:
        config_filefunctions.zoom_level_down()

@touch.C.press()
def touch_c(channel):
    global flag
    flag = 0
    lights.blue.on()
    config_filefunctions.flip_sound()

@touch.release()
def release(channel):
    lights.blue.off()
    print(flag)
    if flag and config_filefunctions.is_unicornhat_inverted() > -1:
        if not os.path.exists(file_name):
            unicorn_bars_calculate.ubars_write()
            os.mknod(file_name)

# waits until a signal is received
signal.pause()
