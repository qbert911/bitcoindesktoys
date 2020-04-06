#!/bin/bash

git pull
cat changelog.txt
exec "/home/pi/bitcoindesktoys/heartbeat.sh"
