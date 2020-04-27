#!/usr/bin/env python
"""
high level support for doing this and that.
"""
import sys
import rainbowhat
rainbowhat.rainbow.set_clear_on_exit(False)

def main():
    rainbowhat.display.clear()

    vala = sys.argv[1]

    rainbowhat.display.print_str(vala)
    rainbowhat.display.show()

if __name__ == "__main__":
    main()
