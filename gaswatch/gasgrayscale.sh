#!/bin/bash
clear
while : ;do
  gasis=$(./gas.py)
  if [[ "$gasis" -ne "$gaswas" ]];then
    if [[ "$gasis" -lt "100" ]] && [[ "$gaswas" -ge "100" ]];then clear;fi  #screen needs cleaning when going from three down to two digits
    if [[ "$gasis" -ge "10" ]] && [[ "$gaswas" -lt "10" ]];then clear;fi  #screen needs cleaning when going from three down to two digits
    if [[ "${gasis: -1}" -eq "1" ]] && [[ "${gaswas: -1}" -ne "1" ]];then clear;fi  #screen needs cleaning when going from three down to two digits
    gaswas=$gasis
    echo -e "\033[3;0H"
    echo -e $(echo -e $gasis) | figlet -f "s-relief" -c -t
    echo -e "\e[?25l"
  fi
  sleep 15  

done
