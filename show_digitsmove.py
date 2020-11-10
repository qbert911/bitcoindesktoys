#!/usr/bin/env python
"""
rainbow HAT - alter digits and call led function
"""
# pylint: disable=C0103,W0702,C0301
import sys
from time import time, sleep
import microdotphat
import rainbowhat
from rainbowhat_ledfunctions import rainbow_show_float, rainbow_show_message, rainbow_led_pricechange
from config_filefunctions import is_sound_on

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


counter = 1.0
soundon = is_sound_on()
try:
    rainbowhat.lights.red.off()    #hack for starting led
except:
    pass

if vala > valb:
    stride = -1
    Note_Freq = 82
    #if soundon:
    try:
        rainbowhat.lights.red.on()
    except:
        pass
else:
    stride = 1
    Note_Freq = 2
    #if soundon:
    try:
        rainbowhat.lights.green.on()
    except:
        pass

for val in range(vala, valb+stride, stride):
    sleep_time = min((counter/(abs(vala-valb)+1.000))**1.8*(10.0/(abs(vala-valb)+1.0)), 3.000)
    #print(sleep_time,val)

    if soundon:
        try:
            rainbowhat.buzzer.midi_note(Note_Freq, .05)
        except:
            pass

    try:
        if valc > 999:
            mystring = "0"+(str(val).rjust(len(str(val)))[0:2+len(str(val))-5] + str(val)[-3+len(str(val).rjust(5))-5:]).rjust(5)
            rainbow_show_float(float("0."+str(val)[0:3]))
            rainbow_led_pricechange(0)
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
