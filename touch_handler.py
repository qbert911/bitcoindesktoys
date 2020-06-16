#!/usr/bin/env python
"""
rainbow hat - touch handler
"""
# pylint: disable=C0116,E1101,W0613
import signal
import rainbowhat
import config_filefunctions
rainbowhat.rainbow.set_clear_on_exit(False)

@rainbowhat.touch.A.press()
def touch_a(channel):
    config_filefunctions.zoom_level_up()
    rainbowhat.lights.rgb(1, 0, 0)

@rainbowhat.touch.B.press()
def touch_b(channel):
    config_filefunctions.zoom_level_down()
    rainbowhat.lights.rgb(0, 1, 0)

@rainbowhat.touch.C.press()
def touch_c(channel):
    config_filefunctions.flip_sound()
    rainbowhat.lights.rgb(0, 0, 1)

@rainbowhat.touch.release()
def release(channel):
    rainbowhat.lights.rgb(0, 0, 0)

# waits until a signal is received
signal.pause()
