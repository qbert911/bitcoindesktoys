#!/bin/bash

until nc -zw1 www.google.com 443 &>/dev/null;do sleep 3;done
  cd /home/pi/bitcoindesktoys
  git pull
	
 cat /home/pi/bitcoindesktoys/changelog.txt
exec "/home/pi/bitcoindesktoys/heartbeat.sh"
read -n1 -r -p "Press space to continue..." key
