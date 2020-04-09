#!/bin/bash

lastreading=$((0))
lastdisplay=$((0))
change=$((0))

while : ;do
  usdreading=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo $usdreading | grep -q "bitcoin"  ;then  #data scrape was successful
    usdreading=$(echo $usdreading |jq -r '.bitcoin.usd')
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
  else
    usdreading=$lastreading
  fi

  if [[ "$usdreading" = "$lastdisplay" ]];then
    echo -en "."
  else
    if [[ "$usdreading" > "$lastdisplay" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($changeup-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    eval "/home/pi/bitcoindesktoys/show_message.py $(printf '%04.0f' $usdreading)"
    echo -en "\n$changeup $change $usdreading $(date)"
    lastdisplay=$usdreading
    eval "/home/pi/bitcoindesktoys/led_pricechange.py $change"
  fi
  lastreading=$usdreading
  sleep 10
done
