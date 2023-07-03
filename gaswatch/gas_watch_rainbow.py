#!/usr/bin/env python3
"""gas"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import optparse
import time
import lolcat
import price_grab_to_output

options = optparse.OptionParser()   #make use of optparse object class as lolcat expects it
options.animate = options.force = False
options.freq = 0.1
char_lengths = {'0': 25.5, '1': 20, '2': 28, '3': 27, '4': 29, '5': 30, '6': 28, '7': 28, '8': 28, '9': 29}

def main():
    options.spread = 3.0
    delay = 0.07
    lines_down = 5
    cycles = y = 3
    x = length = price_string = 999

    while True:
        if x > 248:
            x = 1
            y = y + 1
            if y > cycles:
                price_string = price_grab_to_output.dograb()  #use web3 to get eth gas price
                length_old = length
                length = y = 0
                for i in range(len(price_string)):
                    try:
                        length = length + char_lengths.get(price_string[i]) - 10
                    except Exception:
                        length = 0
                if length < length_old or (length <= length_old + 1 and price_string[i] == '5') \
                                       or (length == length_old and price_string[i] == '1') \
                                       or length_old > 50:  #five character has wierd ending
                    myarray=[]
                    print("\033c")  #clear screen

                myarray.append(f"{price_string} ({length})")
                if len(myarray) > 5:
                    del myarray[0]
                if length > 50:
                    price_string = f"{price_string[0:2]}." #truncate longer price strings so as to not bleed of edge of
                price_grab_to_output.dofiglet(price_string)
        print("\033[0;0H \033[0;0m", myarray,"    ")  #debug message
        x = x + 1
        options.os = 252 - x
        print("\033[?25l \033[0;0H", "\n"*lines_down)  #move cursor to top of screen
        with open("output.txt", 'r') as handle:
            lolcat.LolCat().cat(handle, options)       #draw rainbow digits
        time.sleep(delay)
if __name__ == "__main__":
    main()
