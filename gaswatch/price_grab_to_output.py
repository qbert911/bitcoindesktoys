#!/usr/bin/env python3
"""gas"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import os
import logging
logging.getLogger().disabled = True
from web3 import Web3

def doit(font='s-relief'):
    myval=str(round(Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/753484fba9304da39c9c724e8b8dfccf')).eth.gasPrice/10**9))
    os.system("figlet -f '"+font+"' -c -t "+myval+" >output.txt")
    return myval

if __name__ == "__main__":
    doit()
