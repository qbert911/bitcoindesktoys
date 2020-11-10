#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import time
import json
from requests import Session
from colorama import Fore, Style, init
init()

url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
parameters = {'amount':'1', 'id':'6538', 'convert':'USD'}
headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': 'cb83ec9c-8b44-4f79-b62c-66ec167bd4b2'}
session = Session()
session.headers.update(headers)
file_nameh = "ghistoryh.json"
usym = Fore.YELLOW + Style.BRIGHT + "$" + Fore.GREEN
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def show_me(inputs, inpute, update, isprice):
    USD = float(isprice)
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)

    while update and USD == 1:
        USD = float(update_price())
        time.sleep(1)

    a = USD * (myarrayh[inputs]["claim"] - myarrayh[inpute]["claim"]) #PROFIT
    b = (myarrayh[inputs]["raw_time"] - myarrayh[inpute]["raw_time"]) / (60*60) #hours elapsed
    c = round(a/b * 24*365 / 6081.51 * 100, 2)  #APR

    print("At $" + Fore.YELLOW + str(format(USD, '.3f')) + Style.RESET_ALL + " per CRV = ", end='')
    print(usym + str(format(round(a/b, 4), '.4f')) + Style.RESET_ALL + "/" + csym + str(format(a/b/USD, '.4f')) + Style.RESET_ALL + " per hour", end=' - ')
    print(usym + str(format(round(24*a/b, 4), '.2f')) + Style.RESET_ALL + "/" + csym + str(format(24*a/b/USD, '.2f')).zfill(5) + Style.RESET_ALL + " per day", end=' - ')
    print(usym + str(format(round(365*24*a/b, 4), '.2f')).zfill(7)  + Style.RESET_ALL + "/" + csym + str(format(365*24*a/b/USD, '.2f')).zfill(5) + Style.RESET_ALL + " per year", end=' - ')
    print(Fore.GREEN + Style.BRIGHT + str(format(c, '.2f')) + Style.RESET_ALL + "/" + Fore.CYAN + str(format(c/USD, '.2f')) + Style.RESET_ALL + "% APR", end=' - ')
    if not update:  #print subtotals
        #print(usym + str(format(round(a, 2), '.2f')).zfill(5) + Style.RESET_ALL + "/" + csym + str(format(a/USD, '.2f')).zfill(5) + Style.RESET_ALL, "profit in", str(round(b)).zfill(3), "hours", end=' - ')
        print(str(round(b)).zfill(3), "hours", end=' - ')
    print("between", myarrayh[inpute]["human_time"], "and", myarrayh[inputs]["human_time"])

    return b

def update_price():
    try:
        response = session.get(url, params=parameters)
        if "price" not in response.text:
            return 1
        return json.loads(response.text)["data"]["quote"]["USD"]["price"]
    except:
        return 1
    return 1

def daily_log(isprice):
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)
    offset = len(myarrayh)-1-(int((len(myarrayh)-1)/24)*24)
    for x in range(0, int((len(myarrayh)-1)/24)):
        round(show_me((x*24)+24+offset, (x*24)+offset, 0, isprice))

if __name__ == "__main__":
    show_me(-1, 0, 0, update_price())
    print("    ")
    daily_log(update_price())
    print("")
