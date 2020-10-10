#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914
import json
import time
from web3 import Web3
from colorama import Fore, Style, init
init()
from curve_log_process import show_me
with open("abi_bfcf.json", 'r') as openfile:
    abiguage = json.load(openfile)

"""
min veCRV for 2.5x boost: 245.?
veCRV balance: 248.?
Current boost: 2.5000
pool Liquidity gauge  CRV APY: 43.11%
#Gauge relative weight: 27.30%
#Minted CRV from this gauge: 0.32

#Liquidity utilization: 10.21% [?]
DAI+USDC+USDT: 297,521,976.47
Daily USD volume: $30,371,612.65
"""
file_name = "ghistory.json"
file_nameh = "ghistoryh.json"
history_lengthm = 61
#myarray = []
#myarrayh = []

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

    raw_balanceof = contract.functions.balanceOf(MY_WALLET_ADDRESS).call()
    balanceof = round(raw_balanceof/1000000000000000000, 2)
    print(Fore.CYAN+"Held 3pool tokens:"+Style.RESET_ALL, Style.BRIGHT+str(balanceof)+Style.RESET_ALL)

    while True:
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        raw_time = round(time.time())
        blocknumber = w3.eth.blockNumber
        raw_claimable = contract.functions.claimable_tokens(MY_WALLET_ADDRESS).call()
        claimable = round(raw_claimable/1000000000000000000, 4)

        mydict = {"raw_time" : raw_time, "human_time": month+"/"+day+" "+hour+":"+minut, "block" : blocknumber, "raw" : raw_claimable, "claim" : claimable, "newc" : round(claimable - myarray[-1].get("claim"), 4)}

        if month+"/"+day+" "+hour+":"+minut != myarray[-1].get("human_time"):
            myarray.append(mydict)
        else:
            print("skip writing as only", Fore.RED+str(raw_time - myarray[-1].get("raw_time"))+Style.RESET_ALL, "seconds elapsed")

        print("  "+str(format(round((myarray[-1].get("claim")-myarray[-61].get("claim"))*24*365/balanceof*100, 2), '.2f'))+" % apr", end='')
        print("  "+format((round(myarray[-1].get("claim")-myarray[-61].get("claim"), 4)), '.4f'), "$ per hour", end=' - ')
        print(myarray[-1].get("human_time"), str(format(myarray[-1].get("newc"), '.4f')), format(claimable, '.4f'), end='')
        #print(" ($"+str(round((myarray[-1].get("claim")-myarray[-61].get("claim"))*24*365,3)),"per year) ", end = '')
        print("      ", end='\r', flush=True)

        with open(file_name, "w") as outfile:
            if len(myarray) > history_lengthm:
                del myarray[0]
            json.dump(myarray, outfile, indent=4)

        if minut == "00":
            myarrayh.append(mydict)
            with open(file_nameh, "w") as outfile:
                json.dump(myarrayh, outfile, indent=4)
            show_me(-2, 1, 0)

        time.sleep(60)

if __name__ == "__main__":
    main()
