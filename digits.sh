#!/bin/bash
lastreading=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json" |jq -r '.bitcoin.usd')
lastdisplay=$(printf '%04.0f' $lastreading)
change=$((0))
START=$(date +%s)
echo -en "Watching BTC price movements."
eval "/home/pi/bitcoindesktoys/show_message.py Load"
while : ;do
  usdreading=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo $usdreading | grep -q "bitcoin"  ;then  #data scrape was successful
    usdreading=$(echo $usdreading |jq -r '.bitcoin.usd')
    usdreading=$(printf '%04.0f' $usdreading)
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
  else
    usdreading=$lastreading
  fi

  if [[ "$usdreading" = "$lastdisplay" && "$change" != "0" ]];then
    echo -en "."
  else
    if [[ "$usdreading" > "$lastdisplay" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($change-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    eval "/home/pi/bitcoindesktoys/show_digitschange.py $lastdisplay $usdreading"
    eval "/home/pi/bitcoindesktoys/led_pricechange.py $change"
    echo -en "\n\$$usdreading $(printf '%+03d' $changeup)/$change $(printf '%+04d' $(( $usdreading - $lastdisplay )) )\$ change  $(( $(date +%s) - $START )) seconds"
    lastdisplay=$usdreading
    START=$(date +%s)
  fi
  lastreading=$usdreading
  sleep 10
done
