#!/bin/bash
echo -en "" > /home/pi/hdbars.csv
value=( $(cut -d ',' -f4 /home/pi/uniswaplog.csv ) )
t=$((0))
if [[ "${#value[@]}" -gt 16 ]];then
  for i in {16..1}; do
    t=$(echo "$t + ( ${value[$(( 0 - $i ))]} *100 - ${value[$(( -1 - $i ))]} *100 )" | bc -l)
    myvalue=$(printf "%.0f " $(echo "${value[$(( 0 - $i ))]} *100 - ${value[$(( -1 - $i ))]} *100" | bc))
    echo -en "$myvalue," >> /home/pi/hdbars.csv
  done
  mv2=$(printf "%.2f" $(echo "$t / 16" | bc -l))
  echo "$mv2" >> /home/pi/hdbars.csv
else
  echo "${#value[@]}"
fi
