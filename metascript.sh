#!/bin/bash

until nc -zw1 1.1.1.1 443 &>/dev/null;do sleep 3;done
  cd /home/pi/bitcoindesktoys
  sudo -u pi git pull

exec "/home/pi/bitcoindesktoys/heartbeat.sh"
read -n1 -r -p "Press space to continue..." key
