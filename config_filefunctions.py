#!/usr/bin/env python
"""
blah
"""
import json
import os
from rainbowhat_ledfunctions import rainbow_show_message

def flip_sound():
    """asdasd"""

    file_name = "/home/pi/config.json"

    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"sound":1}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)

    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        if myfile["sound"] == 1:
            myfile["sound"] = 0
            rainbow_show_message("Mute")
        else:
            myfile["sound"] = 1
            rainbow_show_message("SndY")

        with open(file_name, "w") as outfile:
            json.dump(myfile, outfile)

def is_sound_on():
    """asdasd"""
    file_name = "/home/pi/config.json"
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        return myfile["sound"]

if __name__ == "__main__":
    flip_sound()
    x = is_sound_on()
    print(x)
