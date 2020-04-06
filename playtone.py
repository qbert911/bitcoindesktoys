#!/usr/bin/env python
import rainbowhat
import time
rainbowhat.rainbow.set_clear_on_exit(False)
rainbowhat.buzzer.midi_note(74,.1)
time.sleep (.2)
rainbowhat.buzzer.midi_note(34,.15)
