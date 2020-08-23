#!/bin/bash
sudo /etc/init.d/ntp stop
until ping -nq -c3 8.8.8.8; do
   echo "Waiting for network..."
   sleep 3
done
sudo ntpd -gq
sudo /etc/init.d/ntp start
