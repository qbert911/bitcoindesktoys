#!/bin/bash
#/home/pi/Pimoroni/unicornhathd/examples/demo.py &
sudo /home/pi/bitcoindesktoys/touch_handler.py &
sudo /home/pi/bitcoindesktoys/unicorn_handler.py &

( sudo /etc/init.d/ntp stop
until ping -nq -c3 8.8.8.8; do
   echo "Waiting for network..."
done
ntpdate -s time.nist.gov
sudo /etc/init.d/ntp start )&

#until nc -zw1 1.1.1.1 443 &>/dev/null;do sleep 3;done
#sleep 25
#sudo /home/pi/bitcoin/bitcoind -datadir=/home/pi/bitcoin &
