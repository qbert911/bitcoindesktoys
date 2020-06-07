#!/usr/bin/env python
"""
unicorn hat - show scatter plot of price history
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
    unicorn.brightness(.3)  #prints warning
    sys.stdout = oldstdout

def main():
    """asdasd"""

    file_name = "/home/pi/history.json"
    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"history":[9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008, 9009]}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)

    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)

    try:
        hist_chunk_size = int(sys.argv[1])
    except:
        hist_chunk_size = len(myfile["history"])/8

    myfloor = 9999999
    myceiling = 0
    hist_offset = len(myfile["history"]) - 1 - (hist_chunk_size * 8)
    for x in range(hist_offset, len(myfile["history"])):
        myfloor = min(myfloor, myfile["history"][x])
        myceiling = max(myceiling, myfile["history"][x])
    myrange = myceiling - myfloor

    print("   ("+str(myfloor)+" - "+str(myceiling)+")   range:", myrange, "(", (myrange/8.00), "per cell )    ", len(myfile["history"]), "history records ", hist_chunk_size, " history per cell    offset:", hist_offset)

    for x in range(0, 8):
        print(myfile["history"][(x*hist_chunk_size)+hist_offset], myfile["history"][((x+1)*hist_chunk_size)+hist_offset], (x*hist_chunk_size)+hist_offset, ((x+1)*hist_chunk_size)+hist_offset, end='  ')
    print("")

    for y in range(7, -1, -1):
        for x in range(0, 8):
            localmin = 9999999
            localmax = 0
            for histloop in range(0, hist_chunk_size):
                localmin = min(myfile["history"][(x*hist_chunk_size)+histloop+hist_offset], localmin)
                localmax = max(myfile["history"][(x*hist_chunk_size)+histloop+hist_offset], localmax)

            checkpoint = myfloor+((y)*myrange/8.00)
            checkpointb = myfloor+((y+1)*myrange/8.00)
            if min(myfile["history"][(x*hist_chunk_size)+hist_offset], myfile["history"][((x+1)*hist_chunk_size)+hist_offset]) <= checkpointb and \
               max(myfile["history"][(x*hist_chunk_size)+hist_offset], myfile["history"][((x+1)*hist_chunk_size)+hist_offset]) > checkpoint:
                if myfile["history"][(x*hist_chunk_size)+hist_offset] < myfile["history"][((x+1)*hist_chunk_size)+hist_offset]:
                    print("O ", end='')
                    unicorn.set_pixel(x, 7-y, 0, 180, 0)
                else:
                    print("X ", end='')
                    unicorn.set_pixel(x, 7-y, 180, 0, 0)

            elif localmin <= checkpointb and localmax > checkpoint:
                if myfile["history"][(x*hist_chunk_size)+hist_offset] < myfile["history"][((x+1)*hist_chunk_size)+hist_offset]:
                    print("o ", end='')
                    unicorn.set_pixel(x, 7-y, 150, 150, 150)
                else:
                    print("x ", end='')
                    unicorn.set_pixel(x, 7-y, 150, 150, 150)

            else:
                print(". ", end='')
                unicorn.set_pixel(x, 7-y, 0, 0, 0)
        print("")
    unicorn.show()

if __name__ == "__main__":
    main()
    unicorn.atexit._exithandlers = []
