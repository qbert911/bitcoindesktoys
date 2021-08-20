#!/usr/bin/env python
import time
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
#import rainbowtext
rpcuser="bongos"
rpcpassword="goobers"
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpcuser, rpcpassword))

try:
    while True:
        try:
            gooby=rpc_connection.getmempoolinfo()
            gooby2=rpc_connection.getblockchaininfo()
            x = gooby2["blocks"]
            y = round(gooby2["verificationprogress"],5)

            z = gooby["size"]
            a = z % 10000 / 10000.000
            b = z/10000
        except:
            time.sleep(5)
            a,b,x,y,z=0,0,1,2,3

        print(x,y,z,a*16,b)

        time.sleep(2)

except KeyboardInterrupt:
    print("goodbye")
    #unicornhathd.off()

#finally:
    #unicornhathd.off()
