#!/bin/bash
clear
echo -e "\n"
echo -e "\e[?25l"
while : ;do
  gasis=$(./gas.py)
  if [[ "$gasis" -ne "$gaswas" ]];then
    echo -e "$(echo -e $gasis | figlet -f bigmono12 -c -t)"|lolcat
    echo -e "\033[0;0H"
    #echo "                                                          "
    #echo -e "\033[0;0H"
    gaswas=$gasis
  #else
    #echo -n "."
  fi
  sleep 10


done
