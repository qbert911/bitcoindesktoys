#!/usr/bin/env python
"""
unicorn hat - show scatter plot of price history
"""
# pylint: disable=C0103,C0301,E1101
from __future__ import print_function
import json
import sys
from config_filefunctions import get_zoom_level

red = -1
green = +1
gray = 8
blank = 0
reporting = 0

position = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

def ubars_write():
    """asdasd"""
    file_name = "/home/pi/history.json"
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)

    try:
        hist_chunk_size = min(int(sys.argv[1]), len(myfile["history"])/8)
    except:
        hist_chunk_size = min(int(get_zoom_level()), len(myfile["history"])/8)

    myfloor = 9999999
    myceiling = 0
    hist_offset = len(myfile["history"]) - 1 - (hist_chunk_size * 8)
    for x in range(hist_offset, len(myfile["history"])):
        myfloor = min(myfloor, myfile["history"][x])
        myceiling = max(myceiling, myfile["history"][x])
    myrange = myceiling - myfloor

    print("("+str(myfloor)+" - "+str(myceiling)+") range:", myrange, "per cell:", (myrange/8.0), "history records:", len(myfile["history"]), "history per cell:", hist_chunk_size, "offset:", hist_offset)

    if reporting:
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
                    if reporting:
                        print("O ", end='')
                    position[x][7-y] = green
                else:
                    if reporting:
                        print("X ", end='')
                    position[x][7-y] = red

            elif localmin <= checkpointb and localmax > checkpoint:
                if myfile["history"][(x*hist_chunk_size)+hist_offset] < myfile["history"][((x+1)*hist_chunk_size)+hist_offset]:
                    if reporting:
                        print("o ", end='')
                    position[x][7-y] = gray
                else:
                    if reporting:
                        print("x ", end='')
                    position[x][7-y] = gray
            else:
                if reporting:
                    print(". ", end='')
                position[x][7-y] = blank

        if reporting:
            print("")

    print (position)
    file_name = "/home/pi/unicorn.json"
    with open(file_name, "w") as outfile:
        json.dump(position, outfile)

if __name__ == "__main__":
    ubars_write()
