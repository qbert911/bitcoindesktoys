#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411
import time
import json
import sys
import microdotphat
import rainbowhat
from rainbowhat_ledfunctions import rainbow_led_pricechange
rainbowhat.rainbow.set_clear_on_exit(False)

try:
    vala = int(sys.argv[1])
except:
    vala = 0

print(vala)

microdotphat.set_clear_on_exit(False)
microdotphat.set_rotate180(vala)

file_name = "ghistory.json"
oldstring = "0"

def update_led_curve():

    with open(file_name, 'r') as openfile:
        try:
            myarray = json.load(openfile)
            mystring = format((round(myarray[-1]["claim"]-myarray[-61]["claim"], 4)), '.4f')
            mytotal = round(myarray[-1]["claim"], 1)
        except:
            mystring = ""
            mytotal = 0.0

        microdotphat.write_string(mystring, offset_x=0, kerning=False)
        microdotphat.show()
        rainbowhat.display.print_float(mytotal)
        rainbowhat.display.show()

        return mystring

if __name__ == "__main__":
    change = -1
    while True:
        newstring = update_led_curve()
        if newstring != oldstring:
            if newstring > oldstring:
                change = change + 1
            else:
                change = change - 1
            print("\033[1D  ", change)
            change = min(max(change, -10), 10)
            rainbow_led_pricechange(change)
            oldstring = newstring

        print("\033[8D"+newstring, end='  ')
        for i in '▁▂▃▄▅▆▇█▇▆▅▄▃▁ ':
            print('\b' + i, end='', flush=True)
            time.sleep(1)
