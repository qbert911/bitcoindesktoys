#!/usr/bin/env python3
"""
rainbow HAT - alter digits and call led function
"""
# pylint: disable=C0103,W0702,C0301
import sys
from time import time, sleep
import microdotphat
import rainbowhat
import smbus
from rainbowhat_ledfunctions import rainbow_show_float, rainbow_show_message, rainbow_led_pricechange
from config_filefunctions import is_sound_on

import inkyphat
inkyphat.set_rotation(180)
inkyphat.set_colour("black")
myfont = inkyphat.ImageFont.truetype(inkyphat.fonts.FredokaOne, 84)
bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1

rainbowhat.rainbow.set_clear_on_exit(False)
microdotphat.set_clear_on_exit(False)
microdotphat.set_rotate180(False)

def main():
    """asdasd"""
try:
    #sys.stdout.write('time4digits:')
    timeing = time()
    vala = int(sys.argv[1])
    valb = int(sys.argv[2])
    valc = int(sys.argv[3])
except:
    print("Exception reading input")

w, h = myfont.getsize(sys.argv[2])
inkyphat.text(((inkyphat.WIDTH / 2) - (w / 2), 2), sys.argv[2], 1, font=myfont)
inkyphat.show()
counter = 1.0
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
    #if soundon:
    try:
        bus.read_byte(112)         #check to see if rainbow hat is connected
        rainbowhat.lights.green.on()
    except:
        pass

for val in range(vala, valb+stride, stride):
    sleep_time = min((counter/(abs(vala-valb)+1.000))**1.8*(10.0/(abs(vala-valb)+1.0)), 3.000)
    #print(sleep_time,val)
    if soundon:
        try:
#            bus.read_byte(112)         #check to see if rainbow hat is connected
            rainbowhat.buzzer.midi_note(Note_Freq, .05)
        except:
            pass
    try:
        if valc > 29:
            mystring = "0"+(str(val).rjust(len(str(val)))[0:2+len(str(val))-5] + str(val)[-3+len(str(val).rjust(5))-5:]).rjust(5)
            rainbow_show_float(float(val/100))
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
#sys.stdout.write(str(time()-timeing))
#sys.stdout.flush()
#print("")

if __name__ == "__main__":
    main()
