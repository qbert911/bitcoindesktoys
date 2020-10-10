#!/usr/bin/env python
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914
import json
from web3 import Web3
from colorama import Fore, Style, init
init()

with open("abi_bfcf.json", 'r') as openfile:
    abi_bfcf = json.load(openfile)
with open("abi_d533.json", 'r') as openfile:
    abi_d533 = json.load(openfile)
with open("abi_7002.json", 'r') as openfile:
    abi_7002 = json.load(openfile)
with open("abi_bebc.json", 'r') as openfile:
    abi_bebc = json.load(openfile)
with open("abi_6c3f.json", 'r') as openfile:
    abi_6c3f = json.load(openfile)


MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"

CONTRACT_ADDRESS_bebc = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7" #3pool swap address
CONTRACT_ADDRESS_6c3f = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490" #3pool token address

CONTRACT_ADDRESS_bfcf = "0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A" #3pool guage
CONTRACT_ADDRESS_d533 = "0xD533a949740bb3306d119CC777fa900bA034cd52" #CRV TOKEN dao

CONTRACT_ADDRESS_7002 = "0x7002B727Ef8F5571Cb5F9D70D13DBEEb4dFAe9d1" #curve registry address

def main():
    """asdasd"""
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
    contract_bfcf = w3.eth.contract(CONTRACT_ADDRESS_bfcf, abi=abi_bfcf)
    contract_d533 = w3.eth.contract(CONTRACT_ADDRESS_d533, abi=abi_d533)
    contract_bebc = w3.eth.contract(CONTRACT_ADDRESS_bebc, abi=abi_bebc)
    contract_6c3f = w3.eth.contract(CONTRACT_ADDRESS_6c3f, abi=abi_6c3f)
    contract_7002 = w3.eth.contract(CONTRACT_ADDRESS_7002, abi=abi_7002)

    raw_balanceof = contract_bfcf.functions.balanceOf(MY_WALLET_ADDRESS).call()
    balanceof = round(raw_balanceof/1000000000000000000, 2)
    raw_claimable = contract_bfcf.functions.claimable_tokens(MY_WALLET_ADDRESS).call()
    claimable = round(raw_claimable/1000000000000000000, 4)
    test2 = contract_bfcf.functions.totalSupply().call()
    test3 = contract_bfcf.functions.working_balances(MY_WALLET_ADDRESS).call()
    print(test2,test3)
    print(Fore.GREEN+"Held 3pool tokens:"+Style.RESET_ALL, Style.BRIGHT+str(balanceof)+Style.RESET_ALL, claimable)

    totalsupply = contract_d533.functions.available_supply().call() / 1000000000000000000
    rate=contract_d533.functions.rate().call()
    raw_balanceofd=contract_d533.functions.balanceOf(MY_WALLET_ADDRESS).call()
    balanceofd = round(raw_balanceofd/1000000000000000000, 2)
    print(totalsupply,rate,balanceofd)

    a=contract_bebc.functions.A().call()
    b=contract_bebc.functions.get_virtual_price().call()
    c=contract_bebc.functions.coins(0).call()
    d=contract_bebc.functions.balances(0).call()
    e=contract_bebc.functions.coins(1).call()
    f=contract_bebc.functions.balances(1).call()
    g=contract_bebc.functions.coins(2).call()
    h=contract_bebc.functions.balances(2).call()

    print(a,b,c,d,e,f,g,h)

    a=contract_6c3f.functions.balanceOf(MY_WALLET_ADDRESS).call()
    b=contract_6c3f.functions.name().call()
    print(a,b)

    #a=contract_7002.functions.get_pool_coins("hbtc").call()
    #print(a)

if __name__ == "__main__":
    main()
