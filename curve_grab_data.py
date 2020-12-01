#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702
import json
import time
from web3 import Web3
from curve_log_process import show_me, update_price
from colorama import Back, Fore, Style, init
init()
with open("abi_bfcf.json", 'r') as openfile:
    abiguage = json.load(openfile)
with open("abi_d061.json", 'r') as openfile:
    abiminter = json.load(openfile)
with open("abi_d172.json", 'r') as openfile:
    abifulcrum = json.load(openfile)
with open("abi_c7fd.json", 'r') as openfile:
    abicream = json.load(openfile)

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

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"
MINTER_ADDRESS = "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0"

carray = {"name": ["T", "N", "Y", "C", "B", "S", "G"],
          "invested": [6100, 3000, 1000, 1000, 1000, 1000, 1000],
          "address" : ["0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A",    #3pool
                       "0xF98450B5602fa59CC66e1379DFfB6FDDc724CfC4",    #N
                       "0xFA712EE4788C042e2B7BB55E6cb8ec569C4530c1",    #Y
                       "0x7ca5b0a2910B33e9759DC7dDB0413949071D7575",    #Compound
                       "0x69Fb7c45726cfE2baDeE8317005d3F94bE838840",    #B
                       "0xA90996896660DEcC6E997655E065b23788857849",    #Sv2
                       "0xC5cfaDA84E902aD92DD40194f0883ad49639b023"]}   #G
carray["balanceof"] = [0]*len(carray["name"])
carray["raw"] = [0]*len(carray["name"])
carray["minted"] = [0]*len(carray["name"])

def main():
    """monitor various curve contracts"""
    totalinvested = 0
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))

    for i in range(0, len(carray["name"])):
        carray["balanceof"][i] = round(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS).call()/10**18, 2)
        carray["minted"][i] = w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]).call()
        print(carray["name"][i], carray["address"][i], carray["invested"][i], carray["balanceof"][i], round(carray["minted"][i]/10**18, 2))
        totalinvested += carray["invested"][i]
    print(totalinvested, "invested in total.")
    print(round((myarray[-1]["raw_time"]-myarray[-61]["raw_time"])/60)-60, "minutes out of sync.")

    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    while True:
        USD = 1
        while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:
            time.sleep(6)
            month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        while USD == 1:
            try:
                USD = float(update_price())
            except:
                time.sleep(6)

        mydict = {"raw_time" : round(time.time()), "human_time": month+"/"+day+" "+hour+":"+minut,
                  "USD" : USD, "invested" : totalinvested}

        totalraw = 0
        for i in range(0, len(carray["name"])):
            try:
                carray["raw"][i] = w3.eth.contract(carray["address"][i], abi=abiguage).functions.claimable_tokens(MY_WALLET_ADDRESS).call()
            except:
                carray["raw"][i] = 1
            mydict[carray["name"][i]+"pool"] = round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5)
            mydict[carray["name"][i]+"invested"] = carray["invested"][i]
            totalraw += carray["raw"][i] + carray["minted"][i]

        mydict["claim"] = round(totalraw/10**18, 6)
        myarray.append(mydict)

        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)
            with open(file_nameh, "w") as outfile:
                json.dump(myarrayh, outfile, indent=4)
            time.sleep(3)
            show_me(-1, -2, 1, USD, totalinvested) #compare last record with 2nd to last, update price
            time.sleep(3)

        print("At $" + Fore.YELLOW + str(format(USD, '.3f')) + Style.RESET_ALL + " per CRV = ", end='')

        print(Fore.GREEN + Style.BRIGHT+str(format(round((myarray[-1]["claim"]-myarray[-61]["claim"])*USD*24*365/totalinvested*100, 2), '.2f'))+ Style.RESET_ALL+"% APR", end=' ')
        for i in range(0, len(carray["name"])):
            if carray["invested"][i] > 0:
                print(Fore.RED + Style.BRIGHT+ carray["name"][i]+ Style.RESET_ALL+""+str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[-61][carray["name"][i]+"pool"])*USD*24*365/carray["invested"][i]*100, 2), '.2f')), end=' ')

        print("\b - A"+csym+format(myarray[-1]["claim"], '.2f')+Style.RESET_ALL, end=' ')
        print("Y"+csym+format((round((myarray[-1]["claim"]-myarray[-61]["claim"])*24*365, 2)), '.2f').lstrip("0")+Style.RESET_ALL, end=' ')
        print("D"+csym+format((round((myarray[-1]["claim"]-myarray[-61]["claim"])*24, 2)), '.2f').lstrip("0")+Style.RESET_ALL, end=' ')
        print("H"+csym+format((round(myarray[-1]["claim"]-myarray[-61]["claim"], 4)), '.4f').lstrip("0")+Style.RESET_ALL, end=' ')
        #print("M"+csym+format(round(myarray[-1]["claim"] - myarray[-2]["claim"], 4), '.4f').lstrip("0")+Style.RESET_ALL, end='=')
        #for i in range(0, len(carray["name"])):
        #    if carray["raw"][i] > 0:
        #        print(Fore.RED + Style.BRIGHT+ carray["name"][i] + Style.RESET_ALL + str(format(10000*round(myarray[-1][carray["name"][i]+"pool"] - myarray[-61][carray["name"][i]+"pool"], 4), '.0f').zfill(4)), end=' ')

        iusdc_interest = round(w3.eth.contract("0x32E4c68B3A4a813b710595AebA7f6B7604Ab9c15", abi=abifulcrum).functions.nextSupplyInterestRate(1).call()/10**18, 2)
        crcrv_interest = round(((((w3.eth.contract("0xc7Fd8Dcee4697ceef5a2fd4608a7BD6A94C77480", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
        crusdc_interest = round(((((w3.eth.contract("0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
        print("\b - "+Back.CYAN+Fore.BLUE+Style.DIM+"F"+str(iusdc_interest)+"% C"+str(crusdc_interest)+"% "+Fore.MAGENTA + Style.BRIGHT + "Ç"+str(crcrv_interest)+"%"+Style.RESET_ALL, end=' - ')

        if round((myarray[-1]["raw_time"]-myarray[-61]["raw_time"])/60)-60 > 0:
            print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[-61]["raw_time"])/60)-60)+ Style.RESET_ALL, end=' - ')
        print(myarray[-1]["human_time"], end='\r', flush=True)

        with open(file_name, "w") as outfile:
            if len(myarray) > history_lengthm:
                del myarray[0]
            json.dump(myarray, outfile, indent=4)

if __name__ == "__main__":
    main()
