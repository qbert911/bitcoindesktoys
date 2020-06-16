#!/usr/bin/env python
"""
blah
"""
import json
import os
import rainbowhat
from rainbowhat_ledfunctions import rainbow_show_message
rainbowhat.rainbow.set_clear_on_exit(False)

def ensure_config_file_exists(file_name):
    """asdasdasd"""
    if not os.path.isfile(file_name):  #instantiate new config file
        mydict = {"sound":1, "invert_unicornhat":0, "zoom_level":30, "show_speed":1, "column_width":100}
        with open(file_name, "w") as outfile:    #invert_unicornhat: zero for battlestation, 1 for twin display, and -1 for solo
            json.dump(mydict, outfile)

def flip_sound():
    """asdasd"""
    file_name = "/home/pi/config.json"
    ensure_config_file_exists(file_name)
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
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        return myfile["sound"]

def is_unicornhat_inverted():
    """asdasd"""
    file_name = "/home/pi/config.json"
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        return myfile["invert_unicornhat"]

def get_zoom_level():
    """asdasd"""
    file_name = "/home/pi/config.json"
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        return myfile["zoom_level"]

def zoom_level_up():
    """asdasd"""
    file_name = "/home/pi/config.json"
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        if myfile["zoom_level"] < 30:
            myfile["zoom_level"] = myfile["zoom_level"] + 1

        rainbow_show_message(str(myfile["zoom_level"]))

        with open(file_name, "w") as outfile:
            json.dump(myfile, outfile)

def zoom_level_down():
    """asdasd"""
    file_name = "/home/pi/config.json"
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        if myfile["zoom_level"] > 0:
            myfile["zoom_level"] = myfile["zoom_level"] - 1

        rainbow_show_message(str(myfile["zoom_level"]))

        with open(file_name, "w") as outfile:
            json.dump(myfile, outfile)


if __name__ == "__main__":
    zoom_level_up()
    flip_sound()
    print("sound: ", is_sound_on())
