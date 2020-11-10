#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702
import json
import time
from web3 import Web3
from curve_log_process import show_me
from colorama import Fore, Style, init
init()
with open("abi_bfcf.json", 'r') as openfile:
    abiguage = json.load(openfile)

file_name = "ghistory.json"
file_nameh = "ghistoryh.json"
history_lengthm = 61
#myarray = []
#myarrayh = []
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

with open(file_name, 'r') as openfile:
    myarray = json.load(openfile)

with open(file_nameh, 'r') as openfile:
    myarrayh = json.load(openfile)

CONTRACT_ADDRESS = "0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A"
MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"

def main():
    """asdasd"""
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
    contract = w3.eth.contract(CONTRACT_ADDRESS, abi=abiguage)

    balanceof = round(contract.functions.balanceOf(MY_WALLET_ADDRESS).call()/1000000000000000000, 2)
    print(Fore.CYAN+"Held 3pool tokens:"+Style.RESET_ALL, Style.BRIGHT+str(balanceof)+Style.RESET_ALL)

    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    raw_claimable = contract.functions.claimable_tokens(MY_WALLET_ADDRESS).call()
    claimable = round(raw_claimable/1000000000000000000, 4)

    while True:
        while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:
            time.sleep(6)
            month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
            try:
                raw_claimable = contract.functions.claimable_tokens(MY_WALLET_ADDRESS).call()
            except:
                raw_claimable = 1
            claimable = round(raw_claimable/1000000000000000000, 4)
            print("\033[9D"+csym+format(claimable, '.4f')+Style.RESET_ALL, end='', flush=True)

        mydict = {"raw_time" : round(time.time()), "human_time": month+"/"+day+" "+hour+":"+minut, "block" : 0, "raw" : raw_claimable, "claim" : claimable, "newc" : round(claimable - myarray[-1]["claim"], 4)}
        myarray.append(mydict)
        print("\r                                                                             ", end='\r', flush=True)
        print("  "+str(format(round((myarray[-1]["claim"]-myarray[-61]["claim"])*24*365/balanceof*100, 2), '.2f'))+" % apr", end='')
        print("  "+Fore.CYAN+format((round(myarray[-1]["claim"]-myarray[-61]["claim"], 4)), '.4f'), Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL+" per hour", end=' - ')
        print(myarray[-1]["human_time"], str(format(myarray[-1]["newc"], '.4f')), csym+format(claimable, '.4f')+Style.RESET_ALL, end='', flush=True)
        #print(" ($"+str(round((myarray[-1]["claim"]-myarray[-61]["claim"])*24*365,3)),"per year) ", end = '')

        with open(file_name, "w") as outfile:
            if len(myarray) > history_lengthm:
                del myarray[0]
            json.dump(myarray, outfile, indent=4)

        if minut == "00":
            myarrayh.append(mydict)
            with open(file_nameh, "w") as outfile:
                json.dump(myarrayh, outfile, indent=4)
            time.sleep(3)
            print("\r                                                                             ", end='\r', flush=True)
            show_me(-1, -2, 1, 1) #compare last record with 2nd to last, update price
            time.sleep(3)
            
if __name__ == "__main__":
    main()
