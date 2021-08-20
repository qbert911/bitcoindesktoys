#!/usr/bin/env python3
"""
blah
"""
import json
import os
from rainbowhat_ledfunctions import rainbow_show_message

path_current_directory = os.path.dirname(__file__)
path_config_file = os.path.join(path_current_directory, 'config.json')


def ensure_config_file_exists(file_name):
    """asdasdasd"""
    if not os.path.isfile(file_name):  #instantiate new config file
        print("CONFIG FILE NOT FOUND")
        mydict = {"invert_unicornhat":0,  #invert_unicornhat: zero for battlestation..
                    "sound":1,            #..1 for twin display, and -1 for solo
                    "history_length":240,
                    "token_to_track": "curve-dao-token",
                     "token_modifier": 100,
                     "token_modifier_for_microhat": 10000,
                     "offtoken_to_track": "bitcoin",
                     "offtoken_modifier": 1}
        with open(file_name, "w") as outfile:
            json.dump(mydict, outfile)

def is_sound_on():
    """asdasd"""
    file_name = path_config_file
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        try:
            myfile = json.load(openfile)
            return myfile["sound"]
        except:
            return 0

def is_unicornhat_inverted():
    """asdasd"""
    file_name = path_config_file
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        return myfile["invert_unicornhat"]

def get_history_length():
    """asdasd"""
    file_name = path_config_file
    ensure_config_file_exists(file_name)
    with open(file_name, 'r') as openfile:
        myfile = json.load(openfile)
        return myfile["history_length"]

if __name__ == "__main__":
    print("sound: ", is_sound_on())
