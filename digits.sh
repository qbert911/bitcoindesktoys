#!/bin/bash
lastreading="new"
START=$(date +%s)
echo -en "Watching BTC price movements."
while : ;do
  usdreading=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo $usdreading | grep -q "bitcoin"  ;then  #data scrape was successful
    usdreading=$(echo $usdreading |jq -r '.bitcoin.usd')
    usdreading=$(printf '%04.0f' $usdreading)
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
  else
    usdreading=$lastreading
  fi

  if [[ "$usdreading" = "$lastreading" ]] && [[ "$lastreading" -ne "new" ]];then
    echo -en "."
  else
    if [[ "$lastreading" -eq "new" ]];then
      change=$((0))
      eval "/home/pi/bitcoindesktoys/show_message.py $usdreading"
    else
      if [[ "$usdreading" > "$lastreading" ]];then
        changeup=$(($change+1))
        change=$(( $changeup > 10 ? 10 : $changeup ))
      else
        changeup=$(($change-1))
        change=$(( $changeup < -10 ? -10 : $changeup ))
      fi
      eval "/home/pi/bitcoindesktoys/show_digitsmove.py $lastreading $usdreading"
      eval "/home/pi/bitcoindesktoys/led_pricechange.py $change"
      echo -en "\n\$$usdreading $(printf '%+03d' $change) $(printf '%+04d' $(( $usdreading - $lastreading )) )\$ change  $(( $(date +%s) - $START )) seconds"
    fi
    START=$(date +%s)
  fi
  lastreading=$usdreading
  sleep 10
done
