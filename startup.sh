#!/bin/bash
#sudo /home/pi/Pimoroni/unicornhathd/examples/matrix-hd.py &
sudo /home/pi/bitcoindesktoys/touch_handler.py &
sudo /home/pi/bitcoindesktoys/unicorn_handler.py &
sudo /home/pi/bitcoindesktoys/hd_unicorn_handler.py &
sudo /home/pi/bitcoindesktoys/ledshim_mempool.py &
sudo /home/pi/bitcoindesktoys/time_sync.sh &

until nc -zw1 1.1.1.1 443 &>/dev/null;do sleep 3;done
sleep 25
sudo /home/pi/bitcoin/bitcoind -datadir=/home/pi/bitcoin &
