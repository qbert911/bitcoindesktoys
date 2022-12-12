#!/usr/bin/env python3
"""gas"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import os
import logging
logging.getLogger().disabled = True
from web3 import Web3

INFURA_ID = '4f3de96859f141b5a0c6a84e840ab4ec'   #HACK 

def doit(font='s-relief',outfiglet=True): 
    try:
        myval=str(round(Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_ID}')).eth.gasPrice/10**9))
    except:
        myval="xxx"
    if outfiglet:
        os.system("figlet -f '"+font+"' -c -t "+myval+" >output.txt")
    else:
        with open('output.txt', 'w') as b:
            print (myval,file=b)

    return myval

if __name__ == "__main__":
    myvall=doit(outfiglet=False)
    print(myvall)
