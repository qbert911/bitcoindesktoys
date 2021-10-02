#!/usr/bin/env python3
"""
rainbow HAT - alter digits and call led function
"""
# pylint: disable=C0103,W0702,C0301,E0401
import sys
import os
import json
from time import time, sleep
import smbus
import microdotphat
import rainbowhat
from rainbowhat_ledfunctions import rainbow_show_message, rainbow_led_pricechange

bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1

rainbowhat.rainbow.set_clear_on_exit(False)
microdotphat.set_clear_on_exit(False)
microdotphat.set_rotate180(False)

def is_sound_on():
    """asdasd"""
    file_name = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(file_name, 'r') as openfile:
        try:
            myfile = json.load(openfile)
            return myfile["sound"]
        except:
            return 0

def boop_beeps(vala,valb,valc):
    soundon = is_sound_on()
    try:
        bus.read_byte(112)         #check to see if rainbow hat is connected
        rainbowhat.lights.red.off()    #hack for starting led
    except:
        pass

    if vala > valb:
        stride = -1
        Note_Freq = 82
        if soundon:
            try:
                bus.read_byte(112)         #check to see if rainbow hat is connected
                rainbowhat.lights.red.on()
            except:
                pass
    else:
        stride = 1
        Note_Freq = 2
        try:
            bus.read_byte(112)         #check to see if rainbow hat is connected
            rainbowhat.lights.green.on()
        except:
            pass

    return stride, Note_Freq

def main():
    """asdasd"""
    try:
        vala = int(sys.argv[1])
        valb = int(sys.argv[2])
        valc = int(sys.argv[3])
    except:
        print("Exception reading input")

    counter = 1.0
    soundon = is_sound_on()

    stride, Note_Freq = boop_beeps(vala,valb,valc)

    for val in range(vala, valb+stride, stride):
        sleep_time = min((counter/(abs(vala-valb)+1.000))**1.8*(10.0/(abs(vala-valb)+1.0)), 3.000)
        if soundon:
            try:
    #            bus.read_byte(112)         #check to see if rainbow hat is connected
                rainbowhat.buzzer.midi_note(Note_Freq, .05)
            except:
                pass
        try:
            if valc > 29:
                mystring = "0"+(str(val).rjust(len(str(val)))[0:2+len(str(val))-5] + str(val)[-3+len(str(val).rjust(5))-5:]).rjust(5)
                rainbow_show_message('{:04.2f}'.format(val/100))
                rainbow_led_pricechange(valc-100)  #100 for curve currency
                microdotphat.set_decimal(1, 1)
            else:
                mystring = (str(val).rjust(len(str(val)))[0:2+len(str(val))-5] + "," + str(val)[-3+len(str(val).rjust(5))-5:]).rjust(6)
                rainbow_show_message(str(val))
                rainbow_led_pricechange(valc)
            microdotphat.write_string(mystring, offset_x=0, kerning=False)
            microdotphat.show()
        except:
            pass

        counter = counter+1.0
        sleep(sleep_time)

    sleep(.4)   #needed so we can hear the last sound effect

if __name__ == "__main__":
    main()
