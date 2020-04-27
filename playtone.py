#!/usr/bin/env python
"""
high level support for doing this and that.
"""
import time
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

def main():
    """sdasd"""
    rainbowhat.buzzer.midi_note(74, .1)
    time.sleep(.2)
    rainbowhat.buzzer.midi_note(34, .15)

if __name__ == "__main__":
    main()
