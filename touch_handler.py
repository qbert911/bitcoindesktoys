#!/usr/bin/env python
"""
rainbow hat - touch handler
"""
# pylint: disable=C0116,E1101,W0613
import signal
import rainbowhat
import config_filefunctions
import unicorn_bars
rainbowhat.rainbow.set_clear_on_exit(False)

@rainbowhat.touch.A.press()
def touch_a(channel):
    if config_filefunctions.is_unicornhat_inverted() > -1:
        config_filefunctions.zoom_level_up()
        rainbowhat.lights.rgb(1, 0, 0)
        unicorn_bars.ubars()

@rainbowhat.touch.B.press()
def touch_b(channel):
    if config_filefunctions.is_unicornhat_inverted() > -1:
        config_filefunctions.zoom_level_down()
        rainbowhat.lights.rgb(0, 1, 0)
        unicorn_bars.ubars()

@rainbowhat.touch.C.press()
def touch_c(channel):
    config_filefunctions.flip_sound()
    rainbowhat.rainbow.show()
    rainbowhat.lights.rgb(0, 0, 1)

@rainbowhat.touch.release()
def release(channel):
    rainbowhat.lights.rgb(0, 0, 0)

# waits until a signal is received
signal.pause()
