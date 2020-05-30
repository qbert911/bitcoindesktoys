#!/usr/bin/env python
"""
unicorn hat - show price movement bar charts
"""
# pylint: disable=C0103,C0301
from __future__ import print_function
import json
import os
import sys
import unicornhat as unicorn
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)
with open(os.devnull, 'w') as f:   #to prevent loading message
    oldstdout = sys.stdout
    sys.stdout = f
    unicorn.brightness(0.2)  #prints warning
    sys.stdout = oldstdout

def main():
    """asdasd"""

    file_name = "/home/pi/history.json"

    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"history":[9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008, 9009]}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)
    else:
        with open(file_name, 'r') as openfile:
            myfile = json.load(openfile)

    myfloor = 9999999
    myceiling = 0
    for x in range(len(myfile["history"])-9, len(myfile["history"])):
        myfloor = min(myfloor, myfile["history"][x])
        myceiling = max(myceiling, myfile["history"][x])
    myrange = myceiling - myfloor
    print("   range:", myrange, "      ("+str(myfloor)+" - "+str(myceiling)+")")

    for x in range(len(myfile["history"])-9, len(myfile["history"])-1):
        print(x-(len(myfile["history"])-9), x, myfile["history"][x], myfile["history"][x+1], "{:+04d}".format(myfile["history"][x+1] - myfile["history"][x]), " ", end='')
        for y in range(0, 8):
            checkpoint = myfloor+((y)*myrange/8)+min(y, 1)
            checkpointb = myfloor+((y+1)*myrange/8)
            if min(myfile["history"][x], myfile["history"][x+1]) < checkpointb and max(myfile["history"][x], myfile["history"][x+1]) >= checkpoint:
                if myfile["history"][x] < myfile["history"][x+1]:
                    print("o ", end='')
                    unicorn.set_pixel(x-(len(myfile["history"])-9), 7-y, 0, 255, 0)
                else:
                    print("x ", end='')
                    unicorn.set_pixel(x-(len(myfile["history"])-9), 7-y, 255, 0, 0)

            else:
                print(". ", end='')
                unicorn.set_pixel(x-(len(myfile["history"])-9), 7-y, 0, 0, 0)
        print("")

    unicorn.show()

if __name__ == "__main__":
    main()
    unicorn.atexit._exithandlers = []
