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

def ubars_write(dimension, myfilename):
    """asdasd"""
    #dimension = 8
    position = [[0 for x in range(dimension)] for y in range(dimension)]
    file_name = "/home/pi/history.json"
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)

    try:
        hist_chunk_size = min(int(sys.argv[1]), len(myfile["history"])/dimension)
    except:
        hist_chunk_size = min(int(get_zoom_level()), len(myfile["history"])/dimension)

    myfloor = 9999999
    myceiling = 0
    hist_offset = len(myfile["history"]) - 1 - (hist_chunk_size * dimension)
    for x in range(hist_offset, len(myfile["history"])):
        myfloor = min(myfloor, myfile["history"][x])
        myceiling = max(myceiling, myfile["history"][x])
    myrange = myceiling - myfloor

    print("("+str(myfloor)+" - "+str(myceiling)+") range:", myrange, "per cell:", (myrange/dimension * 1.0), "history len:", len(myfile["history"]), "history/cell:", hist_chunk_size, "offset:", hist_offset+1)
    dim=dimension-1
    for y in range(dim, -1, -1):
        for x in range(0, dimension):
            localmin = 9999999
            localmax = 0
            for histloop in range(0, hist_chunk_size):
                localmin = min(myfile["history"][(x*hist_chunk_size)+histloop+hist_offset], localmin)
                localmax = max(myfile["history"][(x*hist_chunk_size)+histloop+hist_offset], localmax)

            checkpoint = myfloor+((y)*myrange/dimension * 1.00)
            checkpointb = myfloor+((y+1)*myrange/dimension * 1.00)
            if min(myfile["history"][(x*hist_chunk_size)+hist_offset], myfile["history"][((x+1)*hist_chunk_size)+hist_offset]) <= checkpointb and \
               max(myfile["history"][(x*hist_chunk_size)+hist_offset], myfile["history"][((x+1)*hist_chunk_size)+hist_offset]) > checkpoint:
                if myfile["history"][(x*hist_chunk_size)+hist_offset] < myfile["history"][((x+1)*hist_chunk_size)+hist_offset]:
                    position[x][dimension-1-y] = green
                else:
                    position[x][dimension-1-y] = red

            elif localmin <= checkpointb and localmax > checkpoint:
                if myfile["history"][(x*hist_chunk_size)+hist_offset] < myfile["history"][((x+1)*hist_chunk_size)+hist_offset]:
                    position[x][dimension-1-y] = gray
                else:
                    position[x][dimension-1-y] = gray
            else:
                position[x][dimension-1-y] = blank

    #print (position)
    file_name = "/home/pi/"+myfilename+".json"
    with open(file_name, "w") as outfile:
        json.dump(position, outfile)

if __name__ == "__main__":
    ubars_write(8, "unicorn")
    ubars_write(16, "unicornhd")
