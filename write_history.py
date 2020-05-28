#!/usr/bin/env python
"""
blah
"""
import json
import os
import sys

def main():
    """asdasd"""

    newinfo = int(sys.argv[1])
    file_name = "/home/pi/history.json"

    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"history":[9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008]}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)

    for x in range(0, 8):
        myfile["history"][x] = myfile["history"][x+1]

    myfile["history"][8] = newinfo
    #print(myfile["history"])

    with open(file_name, "w") as outfile:
        json.dump(myfile, outfile)


if __name__ == "__main__":
    main()
