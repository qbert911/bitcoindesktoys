#!/bin/bash
sudo /home/pi/bitcoindesktoys/digits/unicorn_handler_duo.py &
sudo chown pi /home/pi/history.json
#only used for computer running full btc node for mempool monitoring
#until nc -zw1 1.1.1.1 443 &>/dev/null;do sleep 3;done
#sleep 20
#sudo /home/pi/bitcoindesktoys/ledshim_mempool.py &
#sudo /home/pi/bitcoin/bitcoind -datadir=/home/pi/bitcoin &
