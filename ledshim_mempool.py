#!/usr/bin/env python
"""
color in ledshim according to size of BTC mempool
"""
# pylint: disable=C0103,C0326
import time
import ledshim
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

ledshim.set_clear_on_exit()

def show_graph(vp, r, g, b):
    """asdasd"""
    barlen = vp * ledshim.NUM_PIXELS
    for x in range(ledshim.NUM_PIXELS):
        if barlen < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(barlen, 1.0) * c / 2) + 127 for c in [r, g, b]]
        ledshim.set_pixel(abs((27*invert)-x), r, g, b)
        barlen -= 1

invert=0
rpcuser = "bongos"
rpcpassword = "goobers"
ledshim.set_brightness(0.15)
while True:
    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpcuser, rpcpassword))
        gooby=rpc_connection.getmempoolinfo()
        v = gooby["size"] % 10000 / 10000.000
        j = gooby["size"]/10000
    except:
        gooby,v,j=0,0,9
    #print(v,j)
    show_graph(v, 255, 255, 255)
    if j > 0:
        ledshim.set_pixel(abs((27*invert)-26), 0, 255, 0)
    if j > 1:
        ledshim.set_pixel(abs((27*invert)-24), 0, 255, 0)
    if j > 2:
        ledshim.set_pixel(abs((27*invert)-22), 0, 255, 0)
    if j > 3:
        ledshim.set_pixel(abs((27*invert)-20), 255, 255, 0)
    if j > 4:
        ledshim.set_pixel(abs((27*invert)-18), 255, 255, 0)
    if j > 5:
        ledshim.set_pixel(abs((27*invert)-16), 255, 255, 0)
    if j > 6:
        ledshim.set_pixel(abs((27*invert)-14), 255, 0, 0)
    if j > 7:
        ledshim.set_pixel(abs((27*invert)-12), 255, 0, 0)
    if j > 8:
        ledshim.set_pixel(abs((27*invert)-10), 255, 0, 0)

    ledshim.show()
    time.sleep(1)
