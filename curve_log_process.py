#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
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

def show_me(inpu, update, isprice):
    if update:
        USD = update_price()
    else:
        USD = isprice
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)

    usym = Fore.YELLOW+Style.BRIGHT+"$"+Style.RESET_ALL
    csym = Fore.MAGENTA+Style.BRIGHT+"Ç"+Style.RESET_ALL
    a = USD * (myarrayh[-1].get("claim") - myarrayh[inpu].get("claim"))
    b = (myarrayh[-1].get("raw_time") - myarrayh[inpu].get("raw_time")) / (60*60)
    c = round(a/b * 24*365 / 6081.51 * 100, 2)
    print("At $"+Fore.YELLOW+str(format(USD, '.3f'))+Style.RESET_ALL+" per CRV = ", end='')
    print(usym+Fore.GREEN+Style.BRIGHT+str(format(round(a/b, 4), '.4f'))+Style.RESET_ALL+"/"+csym+Fore.CYAN+str(format(a/b/USD, '.4f'))+Style.RESET_ALL+" per hour", end=' - ')
    print(Fore.GREEN+Style.BRIGHT+str(format(c, '.2f'))+Style.RESET_ALL+"/"+Fore.CYAN+str(format(c/USD, '.2f'))+Style.RESET_ALL+"% APR", end=' - ')
    if not update:  #print subtotals
        print(usym+Fore.GREEN+Style.BRIGHT+str(format(round(a, 2), '.2f')).zfill(5)+Style.RESET_ALL+"/"+csym+Fore.CYAN+str(format(a/USD, '.2f')).zfill(5)+Style.RESET_ALL, "profit in", str(round(b)).zfill(3), "hours", end=' - ')
    print("between", myarrayh[inpu].get("human_time"), "and", myarrayh[-1].get("human_time"))

def update_price():
    try:
        response = session.get(url, params=parameters)
        if "price" in response.text:
            return json.loads(response.text)["data"]["quote"]["USD"]["price"]
        print(response)
        return 1
    except () as e:
        print(e)
        return 1

def main(isprice):
    show_me(0, 0, isprice)
    show_me(-25, 0, isprice)
    show_me(-13, 0, isprice)
    show_me(-7, 0, isprice)
    show_me(-2, 0, isprice)

if __name__ == "__main__":
    main(update_price())
