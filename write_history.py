#!/usr/bin/env python
"""
blah
"""
import json
import os
import sys
from config_filefunctions import get_history_length

def main():
    """asdasd"""

    newinfo = int(sys.argv[1])
    file_name = "/home/pi/history.json"
    history_length = get_history_length()

    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"history":[newinfo, newinfo, newinfo, newinfo, newinfo, newinfo, newinfo, newinfo, newinfo]}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)

    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        if myfile["history"][len(myfile["history"])-1] != newinfo:
            if len(myfile["history"]) <= history_length:
                myfile["history"].append(newinfo)
            else:
                for allcells in range(0, len(myfile["history"])-1):
                    myfile["history"][allcells] = myfile["history"][allcells+1]
                myfile["history"][history_length] = newinfo
            #print(len(myfile["history"]),len(myfile["history"])-9, len(myfile["history"])-1)
            with open(file_name, "w") as outfile:
                json.dump(myfile, outfile)

if __name__ == "__main__":
    main()
