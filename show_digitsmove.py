#!/usr/bin/env python
"""
rainbow HAT - alter digits and call led function
"""
# pylint: disable=C0103
import sys
from time import time, sleep
import rainbowhat
from rainbowhat_ledfunctions import rainbow_led_pricechange, rainbow_show_message
from config_filefunctions import is_sound_on, is_unicornhat_inverted

rainbowhat.rainbow.set_clear_on_exit(False)

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
rainbowhat.lights.red.off()    #hack for starting led

if vala > valb:
    stride = -1
    if soundon:
        rainbowhat.lights.red.on()
else:
    stride = 1
    if soundon:
        rainbowhat.lights.green.on()

for val in range(vala, valb+stride, stride):
    sleep_time = min((counter/(abs(vala-valb)+1.000))**1.8*(10.0/(abs(vala-valb)+1.0)), 3.000)
    #print(sleep_time,val)
    if val > vala:
        if soundon:
            rainbowhat.buzzer.midi_note(82, .05)
    elif val < vala:
        if soundon:
            rainbowhat.buzzer.midi_note(2, .05)

    try:
        rainbow_show_message(str(val))
    except:
        1 == 1

    counter = counter+1.0
    sleep(sleep_time)
if soundon or is_unicornhat_inverted() > -1:
    rainbow_led_pricechange(valc)
sleep(.4)   #needed so we can hear the last sound effect
#sys.stdout.write(str(time()-timeing))
#sys.stdout.flush()
#print("")

if __name__ == "__main__":
    main()
