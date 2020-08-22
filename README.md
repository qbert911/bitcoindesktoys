# bitcoindesktoys
dependencies:
```
ntpd jq curl
```

# .bashrc add
```
vcgencmd get_throttled
grep -ra Pimoroni /proc/device-tree/
sudo i2cdetect -y 1
```

# /etc/rc.local add
```
/home/pi/bitcoindesktoys/startup.sh
```

# backup sd card
```
sudo  pv -tpreb /dev/mmcblk0 | dd of=~/share/img2.img bs=64M
```
