#!/usr/bin/env python3
"""gas"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import logging
logging.getLogger().disabled = True
from web3 import Web3
#INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"
#w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
#print(round(w3.eth.gasPrice/10**9))
print(round(Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/753484fba9304da39c9c724e8b8dfccf')).eth.gasPrice/10**9))
