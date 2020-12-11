#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import json
import time
from web3 import Web3
import microdotphat
from rainbowhat_ledfunctions import rainbow_show_float, rainbow_show_boost_status
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
carray = {"longname": [],
          "invested": [],
          "currentboost": [],
          "name": [],
          "address" : []}

def load_curvepool_array(barray):
    """prepare iteratable array from json file"""
    with open("curvepools.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

    for i in range(0, len(thisarray)):
        barray["longname"].append(thisarray[i]["longname"])
        barray["invested"].append(thisarray[i]["invested"])
        barray["currentboost"].append(thisarray[i]["currentboost"])
        barray["name"].append(thisarray[i]["name"])
        barray["address"].append(thisarray[i]["address"])

    barray["balanceof"] = [0]*len(thisarray)
    barray["raw"] = [0]*len(thisarray)
    barray["minted"] = [0]*len(thisarray)
    barray["totalsupply"] = [0]*len(thisarray)
    barray["futureboost"] = [0]*len(thisarray)
    barray["booststatus"] = [0]*len(thisarray)

def curve_hats_update(myfloat, mystring):
    """output to rainbow and microdot hats"""
    rainbow_show_float(myfloat)
    microdotphat.set_clear_on_exit(False)
    microdotphat.set_rotate180(1)
    microdotphat.write_string(mystring, offset_x=0, kerning=False)
    microdotphat.show()

def boost_check():
    """update variables to check boost status"""
    veCRV_mine = round(w3.eth.contract(veCRV_ADDRESS, abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS).call()/10**18, 2)
    veCRV_total = round(w3.eth.contract(veCRV_ADDRESS, abi=abiguage).functions.totalSupply().call()/10**18, 2)
    myVOTEshare = veCRV_mine/veCRV_total
    hasdata = 0
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] == 2.5:
            carray["booststatus"][i] = -1
            #print(carray["name"][i], end=' ')
            print("", end='')
        else:
            carray["balanceof"][i] = round(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS).call()/10**18, 2)
            carray["totalsupply"][i] = round(w3.eth.contract(carray["address"][i], abi=abiguage).functions.totalSupply().call()/10**18, 2)
            carray["futureboost"][i] = 2.5 * min((carray["balanceof"][i]/2.5) + (carray["totalsupply"][i]*myVOTEshare*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
            if carray["currentboost"][i] >= carray["futureboost"][i]:
                carray["booststatus"][i] = 1
                print("", end='')
                #print(carray["name"][i], end=' ')
                #print(Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(6),
                #      Style.DIM+str(format(carray["futureboost"][i], '.4f')).rjust(6)+" "+
                #      str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(6)+Style.RESET_ALL, end=' - ', flush=True)
            else:
                hasdata = 1
                print(carray["name"][i], end=' ')
                if carray["futureboost"][i]-carray["currentboost"][i] > .01:
                    carray["booststatus"][i] = 2
                    print(#str(format(carray["currentboost"][i], '.4f')).rjust(6),
                        Style.BRIGHT+str(format(carray["futureboost"][i], '.4f')).rjust(6),
                        Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(6)+Style.RESET_ALL, end=' - ')
                else:
                    carray["booststatus"][i] = 3
                    print(str(format(carray["currentboost"][i], '.4f')).rjust(6),
                          Fore.RED+Style.DIM+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(6)+Style.RESET_ALL, end=' - ')

    if hasdata:
        print('\b\b ', end='', flush=True)
    else:
        print(Fore.GREEN+'Boosted'+Style.RESET_ALL, end='', flush=True)
    rainbow_show_boost_status(carray["booststatus"])

def header_display():
    """calculate and display header"""
    eoa = 0 - len(myarray)
    veCRV_mine = round(w3.eth.contract(veCRV_ADDRESS, abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS).call()/10**18, 2)
    veCRV_total = round(w3.eth.contract(veCRV_ADDRESS, abi=abiguage).functions.totalSupply().call()/10**18, 2)
    myVOTEshare = veCRV_mine/veCRV_total
    for i in range(0, len(carray["name"])):
        carray["minted"][i] = w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]).call()
        carray["balanceof"][i] = round(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS).call()/10**18, 2)
        carray["totalsupply"][i] = round(w3.eth.contract(carray["address"][i], abi=abiguage).functions.totalSupply().call()/10**18, 2)
        carray["futureboost"][i] = 2.5*min((carray["balanceof"][i]/2.5) + (carray["totalsupply"][i]*myVOTEshare*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
        print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), carray["name"][i], carray["invested"][i],
              str(format(carray["balanceof"][i], '.2f')).rjust(7), str(format(carray["totalsupply"][i], '.0f')).rjust(9),
              Style.DIM+str(format(round(carray["minted"][i]/10**18, 2), '.2f')).rjust(6)+Style.RESET_ALL,
              Style.DIM+str(format(round(myarray[-1][carray["name"][i]+"pool"]-(carray["minted"][i]/10**18), 2), '.2f')).rjust(6)+Style.RESET_ALL,
              str(format(round(myarray[-1][carray["name"][i]+"pool"], 2), '.2f')).rjust(6),
              str(format(round(myarray[-1][carray["name"][i]+"pool"]/myarray[-1][carray["name"][i]+"invested"]*100, 2), '.2f')).rjust(6)+ "%", end=' ')
        if carray["currentboost"][i] >= 2.5:
            print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(6).replace("0", " ")+Style.RESET_ALL, end=' ')
            print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+ Style.RESET_ALL)
        elif carray["futureboost"][i]-carray["currentboost"][i] < 0:
            print(str(format(carray["currentboost"][i], '.4f')).rjust(6), end=' ')
            print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+ Style.RESET_ALL)
        elif carray["futureboost"][i]-carray["currentboost"][i] > 0:
            print(str(format(carray["currentboost"][i], '.4f')).rjust(6), end=' ')
            if carray["futureboost"][i]-carray["currentboost"][i] > 0.01:
                print(Style.BRIGHT, end='')
            else:
                print(Style.DIM, end='')
            print(Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(7)+ Style.RESET_ALL)
        else:
            print(str(format(carray["currentboost"][i], '.4f')).rjust(6), end=' ')
            print(str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f').rjust(7))+ Style.RESET_ALL)

    print(sum(carray["invested"]), "invested, as well as", veCRV_mine, "veCRV locked (out of", round(veCRV_total), "total).", flush=True)

    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+ Style.RESET_ALL+" minutes out of sync.")
    if eoa > -61:
        print(Fore.RED+str(61+eoa)+ Style.RESET_ALL+" minutes under 60.")
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+ Style.RESET_ALL+" of New investments obscuring data for up to an hour.")

def print_status_line(USD, eoa, totalinvested):
    """print main status line"""
    print("At $" + Fore.YELLOW + str(format(USD, '.3f')) + Style.RESET_ALL + " per CRV = ", end='')
    print(Fore.GREEN + Style.BRIGHT+str(format(round((myarray[-1]["claim"]-myarray[eoa]["claim"])*USD*24*365/totalinvested*100, 2), '.2f'))+ Style.RESET_ALL+"/", end='')
    print(Fore.CYAN +str(format(round((myarray[-1]["claim"]-myarray[eoa]["claim"])*24*365/totalinvested*100, 2), '.2f'))+ Style.RESET_ALL+"% APR", end=' ')

    for i in range(0, len(carray["name"])):
        if carray["invested"][i] > 0:
            print(Fore.RED + Style.BRIGHT+ carray["name"][i]+ Style.RESET_ALL+""+str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])*USD*24*365/carray["invested"][i]*100, 2), '.2f')), end=' ')

    print("\b - A"+csym+format(myarray[-1]["claim"], '.2f')+Style.RESET_ALL, end=' ')
    print("Y"+csym+format((round((myarray[-1]["claim"]-myarray[eoa]["claim"])*24*365, 2)), '.2f').lstrip("0")+Style.RESET_ALL, end=' ')
    print("D"+csym+format((round((myarray[-1]["claim"]-myarray[eoa]["claim"])*24, 2)), '.2f').lstrip("0")+Style.RESET_ALL, end=' ')
    print("H"+csym+format((round(myarray[-1]["claim"]-myarray[eoa]["claim"], 4)), '.4f').lstrip("0")+Style.RESET_ALL, end=' ')
    #print("M"+csym+format(round(myarray[-1]["claim"] - myarray[-2]["claim"], 4), '.4f').lstrip("0")+Style.RESET_ALL, end='=')
    #for i in range(0, len(carray["name"])):
    #    if carray["raw"][i] > 0:
    #        print(Fore.RED + Style.BRIGHT+ carray["name"][i] + Style.RESET_ALL + str(format(10000*round(myarray[-1][carray["name"][i]+"pool"] - myarray[eoa][carray["name"][i]+"pool"], 4), '.0f').rjust(4)), end=' ')

    iusdc_interest = round(w3.eth.contract("0x32E4c68B3A4a813b710595AebA7f6B7604Ab9c15", abi=abifulcrum).functions.nextSupplyInterestRate(1).call()/10**18, 2)
    crcrv_interest = round(((((w3.eth.contract("0xc7Fd8Dcee4697ceef5a2fd4608a7BD6A94C77480", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    #crusdc_interest = round(((((w3.eth.contract("0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    print("\b - "+Back.CYAN+Fore.BLUE+Style.DIM+"F"+str(format(iusdc_interest, '.2f'))+"% "+Fore.MAGENTA+Style.BRIGHT+"Ç"+str(format(crcrv_interest, '.2f'))+"%"+Style.RESET_ALL, end=' - ')  #+"C"+str(crusdc_interest)+"% "

    if round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa >= 0:
        print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1)+Style.RESET_ALL, end=' - ')
    if eoa > -61:
        print(Fore.RED+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' - ')
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(myarray[-1]["invested"] - myarray[eoa]["invested"])+Style.RESET_ALL, end=' - ')
    print(myarray[-1]["human_time"], end=' - ', flush=True)

def main():
    """monitor various curve contracts"""
    load_curvepool_array(carray)
    totalinvested = sum(carray["invested"])
    header_display()
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
#Wait for each minute to pass then update price
    while True:
        while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:
            time.sleep(6)
            month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        USD = 1
        while USD == 1:
            try:
                USD = float(update_price())
            except:
                time.sleep(6)
#UPDATE dictionary
        mydict = {"raw_time" : round(time.time()), "human_time": month+"/"+day+" "+hour+":"+minut,
                  "USD" : USD, "invested" : totalinvested}
        totalraw = 0
        for i in range(0, len(carray["name"])):
            try:
                carray["raw"][i] = w3.eth.contract(carray["address"][i], abi=abiguage).functions.claimable_tokens(MY_WALLET_ADDRESS).call()
                if round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5) - myarray[-1][carray["name"][i]+"pool"] > 10:
                    print("MINTING HAPPENED: Before", carray["minted"][i], end='   After ')
                    carray["minted"][i] = w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]).call()
                    print(carray["minted"][i])
            except:
                carray["raw"][i] = 1
            mydict[carray["name"][i]+"pool"] = round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5)
            mydict[carray["name"][i]+"invested"] = carray["invested"][i]
            totalraw += carray["raw"][i] + carray["minted"][i]

        mydict["claim"] = round(totalraw/10**18, 6)
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
            show_me(-1, -2, 1, USD, 1, 0) #compare last record with 2nd to last, update price, do NOT end line
            time.sleep(3)
            print(" - ", end='')
            boost_check()
            print("")
#update information on hats and screen
        curve_hats_update(round((myarray[-1]["claim"]-myarray[eoa]["claim"])*USD*24*365/totalinvested*100, 2),
                          format((round(myarray[-1]["claim"]-myarray[eoa]["claim"], 4)), '.4f'))
        print_status_line(USD, eoa, totalinvested)
        boost_check()
        print("", end='\r', flush=True)
if __name__ == "__main__":
    main()
