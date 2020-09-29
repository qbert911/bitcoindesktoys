#!/usr/bin/env python
# pylint: disable=C0103,C0301
import json
from time import sleep
from web3 import Web3
with open("abi_guage.json", 'r') as openfile:
    abiguage = json.load(openfile)

def main():
    """asdasd"""
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6aa1a043a9854eaa9fa68d17f619f326'))
    contract = w3.eth.contract("0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A", abi=abiguage)
    last_claimable = 0

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
    a=contract.functions.balanceOf("0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B").call()
    a2 = round(a/1000000000000000000, 4)
    print(a2)

    while True:
        blocknumber = w3.eth.blockNumber
        raw_claimable = contract.functions.claimable_tokens("0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B").call()
        claimable = round(raw_claimable/1000000000000000000, 4)
        new_claimable = round(claimable - last_claimable,4)
        print(blocknumber, raw_claimable, claimable, new_claimable)
        sleep(60)
        last_claimable = claimable

if __name__ == "__main__":
    main()
