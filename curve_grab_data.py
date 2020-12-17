#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import json
import time
import logging
import microdotphat
import sys
from rainbowhat_ledfunctions import rainbow_show_float, rainbow_show_boost_status
from curve_log_process import show_me, update_price
from colorama import Back, Fore, Style, init
init()
logging.getLogger().disabled = True
from web3 import Web3
logging.getLogger().disabled = False

with open("abi_bfcf.json", 'r') as openfile:
    abiguage = json.load(openfile)
with open("abi_d061.json", 'r') as openfile:
    abiminter = json.load(openfile)
with open("abi_5f3b.json", 'r') as openfile:
    abivoting = json.load(openfile)
with open("abi_d172.json", 'r') as openfile:
    abifulcrum = json.load(openfile)
with open("abi_c7fd.json", 'r') as openfile:
    abicream = json.load(openfile)

file_name = "ghistory.json"
file_nameh = "ghistoryh.json"
with open(file_name, 'r') as openfile:
    myarray = json.load(openfile)
with open(file_nameh, 'r') as openfile:
    myarrayh = json.load(openfile)

csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
MINTER_ADDRESS = "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0"
veCRV_ADDRESS = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
carray = {"longname": [], "name": [], "invested": [], "currentboost": [], "address" : []}
TARGET_AMOUNT = 10

def call_me(function):
    """input filtering"""
    x = function.call()
    if isinstance(x, list):
        x = x[0]
    if x < 100000:
        print("\n odd output when calling "+str(function))
    return x

def load_curvepool_array(barray):
    """prepare iteratable array from json file"""
    with open("curvepools.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

    barray["minted"] = [0]*len(thisarray)
    barray["balanceof"] = [0]*len(thisarray)
    barray["raw"] = [0]*len(thisarray)
    barray["totalsupply"] = [0]*len(thisarray)
    barray["futureboost"] = [0]*len(thisarray)
    barray["booststatus"] = [0]*len(thisarray)
    for i in range(0, len(thisarray)):
        barray["longname"].append(thisarray[i]["longname"])
        barray["invested"].append(thisarray[i]["invested"])
        barray["currentboost"].append(thisarray[i]["currentboost"])
        barray["name"].append(thisarray[i]["name"])
        barray["address"].append(thisarray[i]["address"])
        if carray["currentboost"][i] > 0:
            carray["minted"][i] = call_me(w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]))

def curve_hats_update(myfloat, mystring, bootstatusarray):
    """output to rainbow and microdot hats"""
    rainbow_show_float(myfloat)
    rainbow_show_boost_status(bootstatusarray)
    microdotphat.set_clear_on_exit(False)
    microdotphat.set_rotate180(1)
    microdotphat.write_string(mystring, offset_x=0, kerning=False)
    microdotphat.show()

def boost_check(endchar):
    """update variables to check boost status"""
    veCRV_mine = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.totalSupply())/10**18, 2)
    outputflag = 0
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] == 2.5:
            carray["booststatus"][i] = -1
        elif carray["currentboost"][i] == 0:
            carray["booststatus"][i] = 4
        else:
            carray["balanceof"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            carray["totalsupply"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.totalSupply())/10**18, 2)
            if carray["currentboost"][i] > 0:
                carray["futureboost"][i] = 2.5 * min((carray["balanceof"][i]/2.5) + (carray["totalsupply"][i]*veCRV_mine/veCRV_total*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
            if carray["currentboost"][i] >= carray["futureboost"][i]:
                carray["booststatus"][i] = 1
            else:
                outputflag = 1
                print(carray["name"][i], end=' ')
                if carray["futureboost"][i]-carray["currentboost"][i] > .01:
                    carray["booststatus"][i] = 2
                    print(Style.BRIGHT+str(format(carray["futureboost"][i], '.4f')).rjust(6),
                          Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(6)+Style.RESET_ALL, end=' - ')
                else:
                    carray["booststatus"][i] = 3
                    print(str(format(carray["futureboost"][i], '.4f')).rjust(6),
                          Fore.RED+Style.DIM+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(6)+Style.RESET_ALL, end=' - ')

    if outputflag:
        print('\b\b ', end=endchar)
    else:
        print(Fore.GREEN+'Boosted'+Style.RESET_ALL, end=endchar)

def header_display():
    eoa = 0 - len(myarray)
    veCRV_start = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.locked(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_mine = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.totalSupply())/10**18, 2)
    for i in range(0, len(carray["name"])):
        carray["totalsupply"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.totalSupply())/10**18, 2)
        if carray["currentboost"][i] > 0:
            carray["balanceof"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
        maxinvestforfullboost = carray["totalsupply"][i]*veCRV_mine/veCRV_total
        print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), carray["name"][i], str(carray["invested"][i]).rjust(4),
              str(format(carray["balanceof"][i], '.2f')).rjust(7), str(format(carray["totalsupply"][i], '.0f')).rjust(9),
              Style.DIM+str(format(round(carray["minted"][i]/10**18, 2), '.2f')).rjust(7)+Style.RESET_ALL, end='')
        if carray["currentboost"][i] > 0:
            needed_veCRV = round((carray["balanceof"][i]/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            carray["futureboost"][i] = 2.5*min((carray["balanceof"][i]/2.5) + (maxinvestforfullboost*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
            print(Style.DIM+str(format(round(myarray[-1][carray["name"][i]+"pool"]-(carray["minted"][i]/10**18), 2), '.2f')).rjust(7)+Style.RESET_ALL,
                  str(format(round(myarray[-1][carray["name"][i]+"pool"], 2), '.2f')).rjust(6),
                  str(format(round(myarray[-1][carray["name"][i]+"pool"]/myarray[-1][carray["name"][i]+"invested"]*100, 2), '.2f')).rjust(5)+"%", end=' ')
        else:
            needed_veCRV = round((TARGET_AMOUNT/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            print(Style.DIM+str(format(round(0, 2), '.2f')).rjust(7)+Style.RESET_ALL,
                  str(format(round(0, 2), '.2f')).rjust(6),
                  str(format(round(0, 2), '.2f')).rjust(5)+"%", end=' ')

        if carray["currentboost"][i] >= 2.5:
            if carray["futureboost"][i]-carray["currentboost"][i] < 0:
                print(Style.DIM+Fore.GREEN+str(format(abs(round(maxinvestforfullboost-carray["balanceof"][i], 2)), '.2f')).rjust(8)+Style.RESET_ALL, end=' ')
                print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(6).replace("0", " ")+Style.RESET_ALL, end=' ')
                print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+Style.RESET_ALL, end=' ')
                print(Style.DIM+str(needed_veCRV).rjust(4)+Style.RESET_ALL)
            else:
                print(str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(8)+Style.RESET_ALL, end=' ')
                print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(6).replace("0", " ")+Style.RESET_ALL)
        else:
            print(Style.DIM+str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(8)+Style.RESET_ALL, end=' ')
            print(str(format(carray["currentboost"][i], '.4f')).rjust(6), end=' ')
            if carray["futureboost"][i]-carray["currentboost"][i] <= 0:
                print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+Style.RESET_ALL, end=' ')
            else:
                if carray["futureboost"][i]-carray["currentboost"][i] > 0.01:
                    print(Style.BRIGHT+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+Style.RESET_ALL, end=' ')
                else:
                    print(Style.DIM+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+Style.RESET_ALL, end=' ')
            if carray["currentboost"][i] == 0:
                print(str(needed_veCRV).rjust(4), "additional veCRV needed for full boost at target of $"+str(TARGET_AMOUNT))
            else:
                print(str(needed_veCRV).rjust(4), "additional veCRV needed for full boost.")

    print(sum(carray["invested"]), "invested, as well as", veCRV_mine, "veCRV voting"+Style.DIM+" (from", veCRV_start ,"locked)", end='  ')
    print(Style.DIM+"{"+str(round(sum(carray["minted"])/10**18, 2)), "minted /", end=' ')
    print(str(round(myarray[-1]["claim"]-(sum(carray["minted"])/10**18), 2)), "in pools}"+Style.RESET_ALL, end='  ')

    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+" minutes out of sync.", end=' ')
    if eoa > -61:
        print(Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data for up to an hour.", end='')
    print("")

def print_status_line(USD, eoa):
    """print main status line"""
    print("\rAt $"+Fore.YELLOW+str(format(USD, '.3f'))+Fore.WHITE+" per CRV = ", end='')
    print(Fore.GREEN+Style.BRIGHT+str(format(round((myarray[-1]["claim"]-myarray[eoa]["claim"])*USD*24*365/sum(carray["invested"])*100, 2), '.2f'))+Style.NORMAL+"/", end='')
    print(Fore.CYAN+str(format(round((myarray[-1]["claim"]-myarray[eoa]["claim"])*24*365/sum(carray["invested"])*100, 2), '.2f'))+Fore.WHITE+"% APR", end=' ')

    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0:
            print(Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL+str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])*USD*24*365/carray["invested"][i]*100, 2), '.2f')), end=' ')

    print("\b - A"+csym+format(myarray[-1]["claim"], '.3f')+Style.RESET_ALL, end=' ')
    print("H"+csym+format((round(myarray[-1]["claim"]-myarray[eoa]["claim"], 4)), '.4f')+Style.RESET_ALL, end=' ')
    print("D"+csym+format((round((myarray[-1]["claim"]-myarray[eoa]["claim"])*24, 2)), '.2f')+Style.RESET_ALL, end=' ')
    print("Y"+csym+format((round((myarray[-1]["claim"]-myarray[eoa]["claim"])*24*365, 0)), '.0f')+Style.RESET_ALL, end=' ')

    iusdc_interest = round(w3.eth.contract("0x32E4c68B3A4a813b710595AebA7f6B7604Ab9c15", abi=abifulcrum).functions.nextSupplyInterestRate(1).call()/10**18, 2)
    crcrv_interest = round(((((w3.eth.contract("0xc7Fd8Dcee4697ceef5a2fd4608a7BD6A94C77480", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    #crusdc_interest = round(((((w3.eth.contract("0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    print("\b - "+Back.CYAN+Fore.BLUE+Style.DIM+"F"+str(format(iusdc_interest, '.2f'))+"%  "+Fore.MAGENTA+Style.BRIGHT+"Ç"+str(format(crcrv_interest, '.2f'))+"%"+Style.RESET_ALL, end=' - ')  #+"C"+str(crusdc_interest)+"% "
    print(myarray[-1]["human_time"], end=' - ')
    boost_check(" - ")
    if round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa >= 0:
        print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1)+Style.RESET_ALL, end=' - ')
    if eoa > -61:
        print(Fore.RED+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' - ')
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(myarray[-1]["invested"] - myarray[eoa]["invested"])+Style.RESET_ALL, end=' - ')
    print('\b\b', end='')

def main():
    """monitor various curve contracts"""
    load_curvepool_array(carray)
#Print header unless passed any command line argument
    if sys.argv[1:]:
        pass
    else:
        header_display()
#Initiate main program loop
    while True:
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
#Wait for each minute to pass to run again
        while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:
            print(" gas is:", Fore.BLUE+Style.BRIGHT+str(round(w3.eth.gasPrice/10**9)).ljust(3)+Style.RESET_ALL, "    ", "\b"*18, end="", flush=True)
            time.sleep(6)
            month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
#Update price value
        USD = 1
        while USD == 1:
            try:
                USD = update_price()
            except:
                time.sleep(2)
#Update dictionary values
        mydict = {"raw_time" : round(time.time()), "human_time": month+"/"+day+" "+hour+":"+minut,
                  "USD" : USD, "invested" : sum(carray["invested"])}
        for i in range(0, len(carray["name"])):
            if carray["currentboost"][i] > 0:
                carray["raw"][i] = call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.claimable_tokens(MY_WALLET_ADDRESS))
                if abs(round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5) - myarray[-1][carray["name"][i]+"pool"]) > 10:
                    print("MINTING HAPPENED: Before", carray["minted"][i], end='   ')
                    carray["minted"][i] = call_me(w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]))
                    print("After", carray["minted"][i])
            mydict[carray["name"][i]+"pool"] = round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5)
            mydict[carray["name"][i]+"invested"] = carray["invested"][i]
#debug lines next 3
            if carray["currentboost"][i] > 0:
                if myarray[-1][carray["name"][i]+"pool"] > mydict[carray["name"][i]+"pool"]:
                    print("error with lower raw value"+carray["name"][i], myarray[-1][carray["name"][i]+"pool"], mydict[carray["name"][i]+"pool"])

        mydict["claim"] = round((sum(carray["raw"])+sum(carray["minted"]))/10**18, 6)
        myarray.append(mydict)
        if len(myarray) > 61:
            del myarray[0]
        eoa = 0 - len(myarray)
#OUTPUT dictionary TO FILES
        with open(file_name, "w") as outfile:
            json.dump(myarray, outfile, indent=4)

        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)
            with open(file_nameh, "w") as outfile:
                json.dump(myarrayh, outfile, indent=4)
            time.sleep(3)
            print("", end='\r')
            show_me(-1, -2, 1, USD, 1, 0) #compare last record with 2nd to last, update price, do NOT end line
            print(" - ", end='')
            boost_check("            \n")
#update information on hats and screen
        print_status_line(USD, eoa)
        curve_hats_update(round((myarray[-1]["claim"]-myarray[eoa]["claim"])*USD*24*365/sum(carray["invested"])*100, 2),
                          format((round(myarray[-1]["claim"]-myarray[eoa]["claim"], 4)), '.4f'),
                          carray["booststatus"])

if __name__ == "__main__":
    main()
