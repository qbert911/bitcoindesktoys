#!/usr/bin/env python
"""
rainbow HAT - alter digits and call led function
"""
# pylint: disable=C0103
import os
import sys
with open(os.devnull, 'w') as f:   #to prevent pygame loading message
    oldstdout = sys.stdout
    sys.stdout = f
    from pygame import mixer
    sys.stdout = oldstdout
#------------end pygame non display message hack------------------------------
from time import time, sleep
import rainbowhat
from rainbowhat_ledfunctions import rainbow_led_pricechange

rainbowhat.rainbow.set_clear_on_exit(False)

mixer.pre_init(buffer=8192)
mixer.init()
soundup = mixer.Sound('/home/pi/bitcoindesktoys/tickup.wav')
sounddown = mixer.Sound('/home/pi/bitcoindesktoys/tickdown.wav')

def main():
    """asdasd"""
try:
    #rainbowhat.display.clear()
    #sys.stdout.write('time4digits:')
    timeing = time()
    vala = int(sys.argv[1])
    valb = int(sys.argv[2])
    valc = int(sys.argv[3])
    counter = 1.0

    if vala > valb:
        stride = -1
        rainbowhat.lights.red.on()
    else:
        stride = 1
        rainbowhat.lights.green.on()
        rainbowhat.lights.red.off()   #hack to turn off bootup dim light

    for val in range(vala, valb+stride, stride):
        sleep_time = min((counter/(abs(vala-valb)+1.000))**1.8*(10.0/(abs(vala-valb)+1.0)), 3.000)
        #print(sleep_time,val)
        if val > vala:
            #soundup.play()
            rainbowhat.buzzer.midi_note(82, .05)
            #rainbowhat.lights.green.toggle()
        elif val < vala:
            #sounddown.play()
            rainbowhat.buzzer.midi_note(2, .05)
            #rainbowhat.lights.red.toggle()
        rainbowhat.display.print_str(str(val))
        rainbowhat.display.show()
        counter = counter+1.0
        sleep(sleep_time)
    rainbow_led_pricechange(valc)
    sleep(.4)   #needed so we can hear the last sound effect
    #sys.stdout.write(str(time()-timeing))
    #sys.stdout.flush()
    #print("")
except:
    print("EXXXXXXXXXXXXXXXXXCEPTION")

if __name__ == "__main__":
    main()
