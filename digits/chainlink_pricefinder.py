#!/usr/bin/env python3
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import sys
import json
import os.path
from etherscan.contracts import Contract #py_etherscan_api
from web3 import Web3
from ens import ENS
from colorama import Style
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

etherscan_key = 'WXPQDYFIT982E3GPJR9JEHXHNYRADB34BN'   #HACK  My etherscan api key
INFURA_ID = 'bfdd3973b810492db7cb27792702782f'   #HACK
infura_w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_ID}'))
mylocal_w3 = Web3(Web3.HTTPProvider('http://192.168.0.146:8545'))
my_w3_connection = infura_w3
try:
    if not mylocal_w3.eth.syncing:
        my_w3_connection = mylocal_w3
except Exception:
    pass

def load_contract(_contract,chainlink_abi=False):
    abi_contract = _contract
    if chainlink_abi:
        abi_contract = "0x231e764B44b2C1b7Ca171fa8021A24ed520Cde10"       #generic oracle contract abi

    file_name = f"abi/{abi_contract}.json"
    if not os.path.isfile(file_name):
        try:
            _this_abi = Contract(address=abi_contract, api_key=etherscan_key).get_abi()
            print(Style.DIM+"  -- Downloading missing abi for", abi_contract, Style.RESET_ALL)
            json.dump(_this_abi, open(file_name, "w"), indent=4)
        except Exception:
            print("unable to download missing abi for", abi_contract)
    else:
        _this_abi = json.load(open(file_name, 'r'))

    return my_w3_connection.eth.contract(_contract, abi=_this_abi).functions

def get_chainlink_price(currency1, currency2="usd"):
    try:
        contract = load_contract(ENS.fromWeb3(my_w3_connection).address(f"{currency1}-{currency2}.data.eth"),chainlink_abi=True)
        value = contract.latestAnswer().call()/10**8 #contract.decimals().call()
    except:
        value = 0
    return value


if __name__ == "__main__":
    myvall=get_chainlink_price(sys.argv[1])
    print(myvall)