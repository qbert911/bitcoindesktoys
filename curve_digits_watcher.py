#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411
import time
import json
import sys
import microdotphat
import rainbowhat
from rainbowhat_ledfunctions import rainbow_led_pricechange
rainbowhat.rainbow.set_clear_on_exit(False)

try:
    vala = int(sys.argv[1])
except:
    vala = 0

rainbowhat.lights.red.off()    #hack for starting led
rainbowhat.lights.green.off()    #hack for starting led
rainbowhat.lights.blue.off()    #hack for starting led

microdotphat.set_clear_on_exit(False)
microdotphat.set_rotate180(1-vala)

file_name = "ghistory.json"
oldstring = "0"

def update_led_curve():
    with open(file_name, 'r') as openfile:
        begavg=0
        endavg=0
        medavg=0
        try:
            myarray = json.load(openfile)
            for v in range(-1,-6,-1):
                #print(v,v-56,end='')
                #begavg += myarray[v]["claim"]/5
                #endavg += myarray[v-56]["claim"]/5
                medavg += (myarray[v]["claim"]-myarray[v-56]["claim"])/5
            #print(begavg,endavg,begavg-endavg,medavg,flush=True)
            mystring = format(round(myarray[-1]["claim"]-myarray[-61]["claim"], 4), '.4f')

            myfloat = round((myarray[-1]["claim"]-myarray[-61]["claim"])*myarray[-1]["USD"]*24*365/myarray[-1]["invested"]*100, 2)
            rainbowhat.display.print_float(myfloat)
            rainbowhat.display.show()
        except:
            mystring = "0.0"
            myfloat = 0.0
    return mystring, myfloat, format(round(medavg*60/56,4), '.4f')

if __name__ == "__main__":
    change = -1
    historyarray = []
    while True:
        newstring, newfloat, medavg = update_led_curve()
        if newstring != oldstring and float(newstring) > 0:
            historyarray.append(float(newstring))
            if len(historyarray) > 10:
                del historyarray[0]
            if newstring > oldstring:
                change = change + 1
            else:
                change = change - 1
            print("\033[1D  ", change)
            change = min(max(change, -10), 10)
            rainbow_led_pricechange(change)
            oldstring = newstring

        print("\r", newstring, medavg, str(newfloat).zfill(2), round(sum(historyarray)/len(historyarray), 4), historyarray, end='  ')
        microdotphat.write_string(format(round(sum(historyarray)/len(historyarray), 4), '.4f'), offset_x=0, kerning=False)
        microdotphat.show()
        for z in '▁▂▃▄▅▆▇█▇▆▅▄▃▁ ':
            print('\b' + z, end='', flush=True)
            time.sleep(.5)
