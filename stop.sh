#!/bin/bash
/home/pi/bitcoin/bitcoin-cli -datadir=/home/pi/bitcoin stop
tail -n 20 -f /home/pi/bitcoin/debug.log
