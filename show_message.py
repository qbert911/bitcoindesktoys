#!/usr/bin/env python

import sys
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

rainbowhat.display.clear()

vala = sys.argv[1]

rainbowhat.display.print_str(vala)
rainbowhat.display.show()
