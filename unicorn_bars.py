#!/usr/bin/env python
"""
blah
"""
import json
import os
import sys

def main():
    """asdasd"""

    file_name = "/home/pi/history.json"

    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"history":[9001,9002,9003,9004,9005,9006,9007,9008]}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)
    else:
        with open(file_name, 'r') as openfile:
            myfile = json.load(openfile)

    myrange = max(myfile["history"])-min(myfile["history"])
    myfloor = min(myfile["history"])
    print ( "minimum is:", min(myfile["history"]), " maximum is: ",max(myfile["history"]) )
    print "range: ", myrange
    print(myfile["history"])

    for y in range(0,8):
        checkpoint = myfloor+((y)*myrange/8)
        checkpointb = myfloor+((y+1)*myrange/8)
        print checkpoint,checkpointb

    for x in range(0,8):
        print(x,myfile["history"][x], myfile["history"][x+1]),
        for y in range(0,8):
            checkpoint = myfloor+((y)*myrange/8)
            checkpointb = myfloor+((y+1)*myrange/8)
            if min(myfile["history"][x], myfile["history"][x+1]) <= checkpointb and max(myfile["history"][x], myfile["history"][x+1]) >= checkpoint:
                if myfile["history"][x] < myfile["history"][x+1]:
                    print "o",
                else:
                    print "x",
            else:
                print ".",
        print ""


if __name__ == "__main__":
      main()
