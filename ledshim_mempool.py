#!/usr/bin/env python
import time 
from sys import exit

import ledshim
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

ledshim.set_clear_on_exit()

def show_graph(vp, r, g, b):
    v = vp * ledshim.NUM_PIXELS
    for x in range(ledshim.NUM_PIXELS):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v, 1.0) * c / 2) + 127 for c in [r, g, b]]
	    #if v < 1:
	    	#print (vp,v,r,g,b)
        ledshim.set_pixel(27-x, r, g, b)
        v -= 1

rpcuser="bongos"
rpcpassword="goobers"
ledshim.set_brightness(0.15)
while True:
    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpcuser, rpcpassword))
        gooby=rpc_connection.getmempoolinfo()
        v = gooby["size"] % 10000 / 10000.000
        j = gooby["size"]/10000
    except:
        gooby,v,j=0,0,8
    #print(v,j)
    show_graph(v, 255, 255, 255)
    if j > 0:
        ledshim.set_pixel(27-26, 0, 255, 0)
    if j > 1:
        ledshim.set_pixel(27-24, 0, 255, 0)
    if j > 2:
        ledshim.set_pixel(27-22, 0, 0, 255)
    if j > 3:
        ledshim.set_pixel(27-20, 0, 0, 255)
    if j > 4:
        ledshim.set_pixel(27-18, 255, 0, 0)
    if j > 5:
        ledshim.set_pixel(27-16, 255, 0, 0)
    if j > 6:
        ledshim.set_pixel(27-14, 255, 0, 255)
    if j > 7:
        ledshim.set_pixel(27-12, 255, 0, 255)

    ledshim.show()
    time.sleep(1)
