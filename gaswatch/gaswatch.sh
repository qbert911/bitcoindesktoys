#!/bin/bash
clear
x="249"
while : ;do
  if [[ "$x" -ge "249" ]];then
    datetime=`TZ='America/New_York' date +"%D %T"`
    x="1"
    gasis=$(./gas.py)
    if [[ "$gasis" -lt "100" ]] && [[ "$gaswas" -ge "100" ]];then clear;fi  #screen needs cleaning when going from three down to two digits
    if [[ "$gasis" -ge "10" ]] && [[ "$gaswas" -lt "10" ]];then clear;fi  #screen needs cleaning when going from three down to two digits
    if [[ "${gasis: -1}" -eq "1" ]] && [[ "${gaswas: -1}" -ne "1" ]];then clear;fi  #screen needs cleaning when going from three down to two digits
    gaswas=$gasis
  else
    sleep .01  #give cpu time off?
  fi
  echo -e "\033[0;0H$datetime\n\n\n\n"
  echo -e $(echo -e $gasis) | figlet -f "s-relief" -c -t | lolcat -S $(echo $((252 - $x)) )
  echo -e "\e[?25l"
  x=$(($x+1))
done
