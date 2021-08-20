# Installation Instructions
Install latest Raspbian OS image
```
sudo apt update

sudo apt-get install jq curl bc git ...

git clone ...

pip install ...

nano /etc/rc.local ...

cp autostart .config/ and remove 2 files if not running btc node

sudo reboot 0
```

# bitcoindesktoys
dependencies:
```
ntpd jq curl bc
pip install python-bitcoinrpc
```
# /etc/rc.local add
```
/home/pi/bitcoindesktoys/startup.sh
```

# .bashrc add
```
vcgencmd get_throttled
grep -ra Pimoroni /proc/device-tree/
sudo i2cdetect -y 1
```

# backup sd card
```
sudo  pv -tpreb /dev/mmcblk0 | dd of=~/share/img2.img bs=64M
```
